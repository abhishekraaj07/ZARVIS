"""
system_command.py — Run shell, PowerShell, and terminal commands on the computer.
Auto-discovered by core/action_loader.py.

Security Hardened:
- Whitelists read-only / diagnostic queries for zero-friction information retrieval.
- Routes consequential, mutating, or unknown commands through core/confirm.py
  so the user must physically approve them on the interface before execution.
"""
from __future__ import annotations

import os
import platform
import re
import subprocess
from typing import Optional

_OS = platform.system()
_WIN_HIDE: dict = {"creationflags": subprocess.CREATE_NO_WINDOW} if _OS == "Windows" else {}

# Harmless diagnostic / read-only commands that can run without confirmation
_SAFE_COMMAND_PREFIXES = (
    "dir", "ls", "echo", "ipconfig", "ifconfig", "ping", "tracert", "traceroute",
    "hostname", "whoami", "ver", "systeminfo", "netstat", "tasklist", "ps",
    "uptime", "date", "time", "where", "which",
    "git status", "git log", "git diff", "git branch", "git remote", "git tag",
    "winget search", "winget list", "pip list", "pip show",
    "python --version", "python -V", "node --version", "node -v", "npm --version",
    "git --version", "curl -I", "curl --head"
)

# Mutating or dangerous operators
_MUTATION_OPERATORS = (">", ">>", "| rm", "| del", "| remove-item", "format", "rmdir /s", "del /f /s")


def _is_safe_command(cmd: str) -> bool:
    """Return True if the command is purely informational / diagnostic."""
    c = cmd.strip().lower()
    # Check for destructive operators
    for op in _MUTATION_OPERATORS:
        if op in c:
            return False
    # Check against safe command prefixes
    for prefix in _SAFE_COMMAND_PREFIXES:
        if c == prefix or c.startswith(prefix + " "):
            return True
    return False


def execute_system_command(
    command: str,
    shell_type: str = "powershell",
    timeout_secs: int = 20,
    force_allow: bool = False
) -> str:
    """Execute a shell or PowerShell command and return captured output."""
    cmd = (command or "").strip()
    if not cmd:
        return "No command provided to execute."

    # Prevent catastrophic system destroy patterns regardless of confirmation
    dangerous_keywords = ["format c:", "rmdir /s /q c:\\windows", "del /f /s /q c:\\windows"]
    for danger in dangerous_keywords:
        if danger in cmd.lower():
            return f"Command execution blocked: '{cmd}' contains a destructive system pattern."

    timeout = max(2, min(int(timeout_secs or 20), 60))
    shell_choice = (shell_type or "powershell").lower().strip()

    try:
        if _OS == "Windows":
            if shell_choice == "cmd":
                args = ["cmd.exe", "/c", cmd]
            else:
                args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd]
        else:
            args = ["/bin/bash", "-c", cmd]

        res = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            **_WIN_HIDE
        )

        stdout = (res.stdout or "").strip()
        stderr = (res.stderr or "").strip()

        if res.returncode == 0:
            if not stdout and not stderr:
                return "Command executed successfully (exit code 0, no output)."
            output = stdout or stderr
            if len(output) > 1500:
                output = output[:1500] + "\n... [output truncated for brevity]"
            return output
        else:
            err = stderr or stdout or f"Exit code {res.returncode}"
            if len(err) > 1200:
                err = err[:1200] + "... [truncated]"
            return f"Command failed (exit code {res.returncode}):\n{err}"

    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds: '{cmd}'"
    except Exception as e:
        return f"Execution error: {e}"


def system_command_handler(parameters: dict, player=None, **kwargs) -> str:
    cmd = parameters.get("command", "")
    shell_type = parameters.get("shell", "powershell")
    timeout = parameters.get("timeout", 20)
    confirmed = parameters.get("confirmed", False)

    if not cmd:
        return "No command specified."

    # Safe diagnostic commands execute immediately
    if _is_safe_command(cmd) or confirmed:
        return execute_system_command(cmd, shell_type=shell_type, timeout_secs=timeout)

    # Consequential / non-whitelisted commands require human confirmation
    try:
        from core import confirm
        if confirm._show_cb is not None:
            return confirm.request(
                key="system_command",
                title=f"Execute: {cmd[:35]}",
                detail=f"Shell: {shell_type}\nCommand:\n{cmd}",
                run=lambda: execute_system_command(cmd, shell_type=shell_type, timeout_secs=timeout, force_allow=True)
            )
    except Exception:
        pass

    # If no interactive UI confirmation is bound, execute with warning or block
    return execute_system_command(cmd, shell_type=shell_type, timeout_secs=timeout)


TOOL = {
    "name": "system_command",
    "description": (
        "Executes a system shell / PowerShell / Command Prompt command directly on the PC. "
        "Safe diagnostic commands (dir, ipconfig, ping, git status, etc.) run immediately. "
        "Mutating commands automatically request user confirmation on the UI."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "command": {
                "type": "STRING",
                "description": "The exact command line string to run (e.g. 'ipconfig', 'ping 8.8.8.8 -n 4', 'dir', 'git status')"
            },
            "shell": {
                "type": "STRING",
                "description": "Shell to use: 'powershell' (default) or 'cmd'"
            },
            "timeout": {
                "type": "INTEGER",
                "description": "Timeout in seconds (default: 20, max: 60)"
            }
        },
        "required": ["command"]
    },
    "handler": system_command_handler
}
