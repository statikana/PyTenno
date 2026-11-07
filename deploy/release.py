"""Automated release & documentation publisher for PyTenno.

Can be invoked by:
- GitHub Actions (`.github/workflows/publish.yml`)
- The local Git `post-commit` hook (`python3 deploy/release.py --publish`)
- Manually (`python3 deploy/release.py --publish [--version X.Y.Z]`)

Steps:
1. Reads the version in ``pyproject.toml``.
2. Checks PyPI (`https://pypi.org/pypi/pytenno/json`) to see if that version is already published.
3. If the version is already on PyPI, automatically increments the patch version
   (e.g., ``2.0.0`` -> ``2.0.1``), unless ``--no-bump`` is passed.
4. Synchronizes the version across ``pyproject.toml``, ``pytenno/__init__.py``, and ``pytenno/client.py``.
5. Regenerates Sphinx documentation files in ``docs/`` via ``deploy/build_documentation.py``.
6. When ``--publish`` is passed:
   - Amends/commits updated version & docs
   - Updates ``v<version>`` tag and pushes ``master`` + tag to GitHub (triggering ReadTheDocs)
   - Builds ``sdist`` and ``wheel`` and uploads to PyPI.
"""

import argparse
import configparser
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from typing import Optional

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PYPROJECT_PATH = os.path.join(ROOT_DIR, "pyproject.toml")
INIT_PATH = os.path.join(ROOT_DIR, "pytenno", "__init__.py")
CLIENT_PATH = os.path.join(ROOT_DIR, "pytenno", "client.py")


def get_local_version() -> str:
    with open(PYPROJECT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise RuntimeError("Could not find version in pyproject.toml")
    return match.group(1)


def get_pypi_versions() -> set[str]:
    req = urllib.request.Request(
        "https://pypi.org/pypi/pytenno/json",
        headers={"User-Agent": "pytenno-release-script"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return set(data.get("releases", {}).keys())
    except Exception as exc:
        print(f"Warning: could not query PyPI releases ({exc})", file=sys.stderr)
        return set()


def bump_patch(version: str) -> str:
    parts = version.split(".")
    if len(parts) < 3 or not parts[-1].isdigit():
        return f"{version}.1"
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def set_version_everywhere(new_version: str) -> None:
    with open(PYPROJECT_PATH, "r", encoding="utf-8") as f:
        pyproject = f.read()
    pyproject = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        pyproject,
        count=1,
        flags=re.MULTILINE,
    )
    with open(PYPROJECT_PATH, "w", encoding="utf-8") as f:
        f.write(pyproject)

    with open(INIT_PATH, "r", encoding="utf-8") as f:
        init_code = f.read()
    init_code = re.sub(
        r'^__version__\s*=\s*"[^"]+"',
        f'__version__ = "{new_version}"',
        init_code,
        count=1,
        flags=re.MULTILINE,
    )
    with open(INIT_PATH, "w", encoding="utf-8") as f:
        f.write(init_code)

    if os.path.exists(CLIENT_PATH):
        with open(CLIENT_PATH, "r", encoding="utf-8") as f:
            client_code = f.read()
        client_code = re.sub(
            r'DEFAULT_USER_AGENT\s*=\s*"pytenno/[^"]+"',
            f'DEFAULT_USER_AGENT = "pytenno/{new_version} (+https://github.com/statikana/pytenno)"',
            client_code,
            count=1,
        )
        with open(CLIENT_PATH, "w", encoding="utf-8") as f:
            f.write(client_code)


def get_pypi_token() -> Optional[str]:
    for env_key in ("PYPI_API_TOKEN", "UV_PUBLISH_TOKEN", "TWINE_PASSWORD"):
        val = os.environ.get(env_key)
        if val:
            return val.strip()
    pypirc = os.path.expanduser("~/.pypirc")
    if os.path.exists(pypirc):
        cfg = configparser.ConfigParser()
        cfg.read(pypirc)
        if cfg.has_option("pypi", "password"):
            return cfg.get("pypi", "password").strip()
    return None


def publish_release(version: str) -> None:
    env = os.environ.copy()
    env["PYTENNO_RELEASE_RUNNING"] = "1"
    if os.path.exists("/etc/ssl/certs/ca-bundle.crt"):
        env.setdefault("SSL_CERT_FILE", "/etc/ssl/certs/ca-bundle.crt")

    subprocess.run(
        ["git", "add", "pyproject.toml", "pytenno/__init__.py", "pytenno/client.py", "docs/"],
        cwd=ROOT_DIR,
        check=True,
    )
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=ROOT_DIR,
    )
    if diff_check.returncode != 0:
        subprocess.run(
            ["git", "commit", "-m", f"chore(release): v{version} [skip ci]"],
            cwd=ROOT_DIR,
            env=env,
            check=True,
        )

    tag_name = f"v{version}"
    subprocess.run(
        ["git", "tag", "-f", "-a", tag_name, "-m", f"Release {tag_name}"],
        cwd=ROOT_DIR,
        check=True,
    )
    subprocess.run(["git", "push", "origin", "master"], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "push", "-f", "origin", tag_name], cwd=ROOT_DIR, check=True)
    print(f"Pushed master and tag {tag_name} to GitHub (ReadTheDocs webhook triggered).")

    dist_dir = os.path.join(ROOT_DIR, "dist")
    shutil.rmtree(dist_dir, ignore_errors=True)

    if shutil.which("uv"):
        subprocess.run(["uv", "build"], cwd=ROOT_DIR, env=env, check=True)
        uv_lock = os.path.join(ROOT_DIR, "uv.lock")
        if os.path.exists(uv_lock):
            os.remove(uv_lock)
        token = get_pypi_token()
        if token:
            subprocess.run(
                ["uv", "publish", "--token", token],
                cwd=ROOT_DIR,
                env=env,
                check=True,
            )
            shutil.rmtree(dist_dir, ignore_errors=True)
            print(f"Published pytenno {version} to PyPI!")
        else:
            print("Warning: No PyPI token found in env or ~/.pypirc; skipped PyPI upload.")
    else:
        subprocess.run([sys.executable, "-m", "build"], cwd=ROOT_DIR, env=env, check=True)
        subprocess.run(["twine", "upload", "--skip-existing", "dist/*"], cwd=ROOT_DIR, env=env, check=True)
        shutil.rmtree(dist_dir, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare & publish PyTenno release & docs.")
    parser.add_argument(
        "--no-bump",
        action="store_true",
        help="Do not auto-increment patch version if local version already exists on PyPI.",
    )
    parser.add_argument(
        "--version",
        type=str,
        default=None,
        help="Explicitly set a target version string (e.g. 2.1.0).",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Commit version/docs, push master & tag (ReadTheDocs), and upload to PyPI.",
    )
    args = parser.parse_args()

    os.chdir(ROOT_DIR)
    current_version = get_local_version()
    published_versions = get_pypi_versions()

    if args.version:
        target_version = args.version
    elif not args.no_bump and current_version in published_versions:
        target_version = bump_patch(current_version)
        while target_version in published_versions:
            target_version = bump_patch(target_version)
        print(
            f"Version {current_version} is already on PyPI; auto-bumping to {target_version}"
        )
    else:
        target_version = current_version
        print(f"Using version {target_version}")

    set_version_everywhere(target_version)

    sys.path.insert(0, os.path.join(ROOT_DIR, "deploy"))
    import build_documentation

    build_documentation.build_files(
        os.path.join(".", "pytenno"),
        os.path.join(".", "docs"),
    )

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as out:
            out.write(f"version={target_version}\n")

    if args.publish:
        publish_release(target_version)


if __name__ == "__main__":
    main()
