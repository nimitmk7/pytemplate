"""
Coverage parser interface module.
Parses coverage data from various formats.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FileCoverage:
    """Represents coverage data for a single file."""
    
    filename: str
    total_lines: int
    covered_lines: int
    coverage_percentage: float
    line_data: dict[int, str]  # line_number -> coverage status


@dataclass
class CoverageData:
    """Complete coverage data for a commit."""
    
    commit_sha: str
    total_coverage: float
    files: dict[str, FileCoverage]


class CoverageParserInterface(ABC):
    """Defines the interface for coverage data parsing."""

    @abstractmethod
    def parse_coverage_xml(self, xml_path: str) -> CoverageData:
        """Parse coverage data from XML file.
        
        Args:
            xml_path: Path to the coverage XML file
            
        Returns:
            Parsed coverage data
        """
        pass  # pragma: no cover

    @abstractmethod
    def set_commit_sha(self, commit_sha: str) -> None:
        """Set the commit SHA for the coverage data.
        
        Args:
            commit_sha: SHA of the commit being analyzed
        """
        pass  # pragma: no cover