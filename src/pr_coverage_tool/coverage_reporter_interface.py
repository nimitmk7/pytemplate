"""
Coverage reporter interface module.
Formats and displays coverage comparison results.
"""
from abc import ABC, abstractmethod
from .pr_coverage_tool_interface import CoverageDelta, LineCoverage


class CoverageReporterInterface(ABC):
    """Defines the interface for coverage reporting."""

    @abstractmethod
    def generate_report(self, delta: CoverageDelta) -> str:
        """Generate a complete coverage report.
        
        Args:
            delta: Coverage delta to report on
            
        Returns:
            Formatted report as string
        """
        pass  # pragma: no cover

    @abstractmethod
    def format_line_coverage(self, file: str, lines: list[LineCoverage]) -> str:
        """Format line-by-line coverage changes.
        
        Args:
            file: File path
            lines: List of line coverage information
            
        Returns:
            Formatted line coverage as string
        """
        pass  # pragma: no cover

    @abstractmethod
    def summarize_changes(self, delta: CoverageDelta) -> str:
        """Generate a summary of coverage changes.
        
        Args:
            delta: Coverage delta to summarize
            
        Returns:
            Summary text
        """
        pass  # pragma: no cover

    @abstractmethod
    def format_as_markdown(self, delta: CoverageDelta) -> str:
        """Format the report as markdown for PR comments.
        
        Args:
            delta: Coverage delta to report on
            
        Returns:
            Markdown formatted report
        """
        pass  # pragma: no cover

    @abstractmethod
    def format_as_json(self, delta: CoverageDelta) -> str:
        """Format the report as JSON for API responses.
        
        Args:
            delta: Coverage delta to report on
            
        Returns:
            JSON formatted report
        """
        pass  # pragma: no cover