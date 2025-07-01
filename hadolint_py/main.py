
import os
import sys
import stat
import platform
import urllib.request
import subprocess

def get_hadolint_version():
    """Gets the hadolint version from the pre-commit ref."""
    ref = os.environ.get("PRE_COMMIT_REF")
    if not ref or not ref.startswith("v"):
        raise ValueError("PRE_COMMIT_REF environment variable not set or invalid.")
    return ref[1:]

def get_platform_info():
    """Gets the platform and architecture."""
    system = platform.system()
    arch = platform.machine()
    return system, arch

def get_download_url(version, system, arch):
    """Constructs the download URL for the hadolint binary."""
    base_url = "https://github.com/hadolint/hadolint/releases/download"
    system_map = {
        "Linux": "Linux",
        "Darwin": "Darwin",
        "Windows": "Windows",
    }
    arch_map = {
        "x86_64": "x86_64",
        "AMD64": "x86_64",
        "aarch64": "arm64",
    }
    hadolint_system = system_map.get(system)
    hadolint_arch = arch_map.get(arch)

    if not hadolint_system or not hadolint_arch:
        raise ValueError(f"Unsupported platform: {system} {arch}")

    return f"{base_url}/v{version}/hadolint-{hadolint_system}-{hadolint_arch}"

def download_hadolint(url, cache_dir):
    """Downloads the hadolint binary to the cache directory."""
    binary_path = os.path.join(cache_dir, "hadolint")
    if not os.path.exists(binary_path):
        print(f"Downloading hadolint from {url}...")
        urllib.request.urlretrieve(url, binary_path)
        st = os.stat(binary_path)
        os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
    return binary_path

def main():
    """Main entry point for the pre-commit hook."""
    try:
        version = get_hadolint_version()
        system, arch = get_platform_info()
        url = get_download_url(version, system, arch)
        
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "hadolint-py")
        os.makedirs(cache_dir, exist_ok=True)

        binary_path = download_hadolint(url, cache_dir)
        
        result = subprocess.run([binary_path] + sys.argv[1:], capture_output=True, text=True)
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        sys.exit(result.returncode)

    except (ValueError, urllib.error.URLError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
