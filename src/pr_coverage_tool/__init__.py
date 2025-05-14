"""PR Coverage Tool package.
This package provides tools for analyzing code coverage changes in pull requests.
"""
# Keeping __init__.py minimal to avoid slowing down imports
from .pr_coverage_tool_interface import (
    PRCoverageToolInterface,
    CoverageReport,
    CoverageDelta,
    PRInfo,
    LineCoverage,
)
from .coverage_parser_interface import (
    CoverageParserInterface,
    CoverageData,
    FileCoverage,
)
from .git_client_interface import GitClientInterface
from .coverage_reporter_interface import CoverageReporterInterface

__all__ = [
    # Interfaces
    "PRCoverageToolInterface",
    "CoverageParserInterface",
    "GitClientInterface",
    "CoverageReporterInterface",
    # Data types
    "CoverageReport",
    "CoverageDelta",
    "CoverageData",
    "PRInfo",
    "LineCoverage",
    "FileCoverage",
]