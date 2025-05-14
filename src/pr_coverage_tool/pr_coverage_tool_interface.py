"""
PR Coverage Tool interface module.
Analyzes code coverage changes in pull requests.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .coverage_parser_interface import CoverageData


@dataclass
class LineCoverage:
    """Represents coverage status for a specific line."""
    
    line_number: int
    before_status: str  # 'covered', 'uncovered', 'not_present'
    after_status: str   # 'covered', 'uncovered', 'not_present'


@dataclass
class CoverageDelta:
    """Coverage difference between two commits."""
    
    total_coverage_before: float
    total_coverage_after: float
    coverage_change: float
    modified_lines: dict[str, list[LineCoverage]]
    files_added: list[str]
    files_removed: list[str]


@dataclass
class PRInfo:
    """Pull request information."""
    
    pr_number: int
    base_branch: str
    head_branch: str
    base_sha: str
    head_sha: str
    repo_url: str


@dataclass
class CoverageReport:
    """Complete PR coverage analysis report."""
    
    pr_info: PRInfo
    coverage_delta: CoverageDelta
    summary: str


class PRCoverageToolInterface(ABC):
    """Defines the interface for PR coverage analysis."""

    @abstractmethod
    def analyze(self, pr_url: str) -> CoverageReport:
        """Analyze coverage changes for a pull request.
        
        Args:
            pr_url: URL of the pull request to analyze
            
        Returns:
            Complete coverage analysis report
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_merge_base(self, base_branch: str, head_branch: str) -> str:
        """Find the merge base commit between two branches.
        
        Args:
            base_branch: The base branch (usually main)
            head_branch: The feature branch
            
        Returns:
            SHA of the merge base commit
        """
        pass  # pragma: no cover

    @abstractmethod
    def compute_coverage(self, commit: str) -> 'CoverageData':
        """Compute code coverage at a specific commit.
        
        Args:
            commit: SHA of the commit to analyze
            
        Returns:
            Coverage data for the commit
        """
        pass  # pragma: no cover

    @abstractmethod
    def compare_coverage(self, before: 'CoverageData', after: 'CoverageData', 
                        modified_lines: dict[str, list[int]]) -> CoverageDelta:
        """Compare coverage data between two commits.
        
        Args:
            before: Coverage data from the base commit
            after: Coverage data from the PR commit
            modified_lines: Dictionary of files to their modified line numbers
            
        Returns:
            Coverage delta between the commits
        """
        pass  # pragma: no cover