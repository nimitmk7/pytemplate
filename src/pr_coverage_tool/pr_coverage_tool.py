"""Implementation of the PR Coverage Tool."""
import subprocess
import tempfile
from pathlib import Path

from .pr_coverage_tool_interface import (
    CoverageDelta,
    CoverageReport,
    LineCoverage,
    PRCoverageToolInterface,
)
from .git_client_interface import GitClientInterface
from .coverage_reporter_interface import CoverageReporterInterface
from .coverage_parser_interface import (
    CoverageParserInterface,
    CoverageData,
)


class PRCoverageTool(PRCoverageToolInterface):
    """Concrete implementation of PR coverage analysis."""
    
    def __init__(
        self, 
        git_client: GitClientInterface, 
        reporter: CoverageReporterInterface,
        coverage_parser: CoverageParserInterface
    ) -> None:
        """Initialize with dependencies.
        
        Args:
            git_client: Git client for repository operations
            reporter: Coverage reporter for generating reports
            coverage_parser: Parser for coverage data
        """
        self.git_client = git_client
        self.reporter = reporter
        self.coverage_parser = coverage_parser
        
    def analyze(self, pr_url: str) -> CoverageReport:
        """Analyze coverage changes for a pull request."""
        # Get PR information
        pr_info = self.git_client.get_pr_info(pr_url)
        
        # Save current state
        current_branch = self.git_client.get_current_branch()
        self.git_client.stash_changes()
        
        try:
            # Get merge base
            merge_base = self.get_merge_base(pr_info.base_branch, pr_info.head_branch)
            
            # Compute coverage at merge base
            self.git_client.checkout(merge_base)
            before_coverage = self.compute_coverage(merge_base)
            
            # Compute coverage at PR head
            self.git_client.checkout(pr_info.head_sha)
            after_coverage = self.compute_coverage(pr_info.head_sha)
            
            # Get modified lines
            modified_files = self.git_client.get_modified_files(
                merge_base, pr_info.head_sha
            )
            modified_lines = {}
            for file in modified_files:
                modified_lines[file] = self.git_client.get_modified_lines(
                    merge_base, pr_info.head_sha, file
                )
            
            # Compare coverage
            coverage_delta = self.compare_coverage(
                before_coverage, after_coverage, modified_lines
            )
            
            # Generate summary
            summary = self.reporter.summarize_changes(coverage_delta)
            
            return CoverageReport(
                pr_info=pr_info,
                coverage_delta=coverage_delta,
                summary=summary
            )
            
        finally:
            # Restore original state
            self.git_client.checkout(current_branch)
            self.git_client.pop_stash()
    
    def get_merge_base(self, base_branch: str, head_branch: str) -> str:
        """Find the merge base commit between two branches."""
        result = subprocess.run(
            ["git", "merge-base", base_branch, head_branch],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    def compute_coverage(self, commit: str) -> CoverageData:
        """Compute code coverage at a specific commit."""
        # Run coverage and generate XML report
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            coverage_xml = tmp.name
            
        try:
            # Install dependencies if needed
            subprocess.run(["uv", "sync"], check=True)
            
            # Determine test paths
            test_paths = []
            if Path("tests").exists():
                test_paths.append("tests")
            if Path("src").exists():
                # Check for test directories in src
                src_tests = list(Path("src").glob("*/tests"))
                test_paths.extend(str(path) for path in src_tests)
            
            if not test_paths:
                test_paths = ["."]  # Fallback to current directory
            
            # Run tests with coverage
            subprocess.run([
                "coverage", "run", "-m", "pytest", *test_paths
            ], check=True)
            
            # Generate XML report
            subprocess.run([
                "coverage", "xml", "-o", coverage_xml
            ], check=True)
            
            # Parse coverage data
            self.coverage_parser.set_commit_sha(commit)
            return self.coverage_parser.parse_coverage_xml(coverage_xml)
            
        finally:
            Path(coverage_xml).unlink(missing_ok=True)
    
    def compare_coverage(
        self, 
        before: CoverageData, 
        after: CoverageData,
        modified_lines: dict[str, list[int]]
    ) -> CoverageDelta:
        """Compare coverage data between two commits."""
        modified_line_coverage = {}
        
        for file, lines in modified_lines.items():
            line_coverage = []
            
            before_file = before.files.get(file)
            after_file = after.files.get(file)
            
            for line_num in lines:
                before_status = 'not_present'
                after_status = 'not_present'
                
                if before_file and line_num in before_file.line_data:
                    before_status = before_file.line_data[line_num]
                    
                if after_file and line_num in after_file.line_data:
                    after_status = after_file.line_data[line_num]
                
                line_coverage.append(LineCoverage(
                    line_number=line_num,
                    before_status=before_status,
                    after_status=after_status
                ))
            
            modified_line_coverage[file] = line_coverage
        
        # Find added/removed files
        before_files = set(before.files.keys())
        after_files = set(after.files.keys())
        
        files_added = list(after_files - before_files)
        files_removed = list(before_files - after_files)
        
        coverage_change = after.total_coverage - before.total_coverage
        
        return CoverageDelta(
            total_coverage_before=before.total_coverage,
            total_coverage_after=after.total_coverage,
            coverage_change=coverage_change,
            modified_lines=modified_line_coverage,
            files_added=files_added,
            files_removed=files_removed
        )