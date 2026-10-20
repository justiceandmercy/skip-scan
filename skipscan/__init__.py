"""skip-scan: find skipped and focused tests in a repository."""

__version__ = "0.1.0"
__all__ = ["scan", "Finding"]

from .scanner import Finding, scan

