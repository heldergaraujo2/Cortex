"""Report basic runtime capabilities without changing the environment or files."""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def _command_version(command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else None


def collect_diagnostics() -> dict[str, object]:
    """Collect non-sensitive host facts; no files are written and no installs are run."""
    disk = shutil.disk_usage(Path.cwd())
    memory_bytes: int | None = None
    try:
        if os.name == "nt":
            output = _command_version(["powershell", "-NoProfile", "-Command",
                                       "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"])
            if output and output.isdigit():
                memory_bytes = int(output)
        else:
            meminfo = Path("/proc/meminfo")
            if meminfo.exists():
                for line in meminfo.read_text(encoding="utf-8").splitlines():
                    if line.startswith("MemTotal:"):
                        memory_bytes = int(line.split()[1]) * 1024
                        break
    except (OSError, ValueError, IndexError):
        memory_bytes = None

    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "git_version": _command_version(["git", "--version"]),
        "cpu_count_logical": os.cpu_count(),
        "memory_bytes": memory_bytes,
        "working_directory_free_bytes": disk.free,
        "working_directory_total_bytes": disk.total,
        "nvidia_smi_version": _command_version(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]),
        "note": "No files were written; GPU details may be null if NVIDIA tooling is unavailable.",
    }


def main() -> None:
    print(json.dumps(collect_diagnostics(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
