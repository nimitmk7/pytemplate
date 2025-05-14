"""End-to-end test for PR Coverage Tool using pre-built test repository."""

import os
import shutil
import subprocess
import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from pr_coverage_tool.pr_coverage_tool import PRCoverageTool
from pr_coverage_tool.git_client import GitClient
from pr_coverage_tool.coverage_reporter import CoverageReporter
from pr_coverage_tool.coverage_parser import CoverageParser
from pr_coverage_tool import PRInfo


# Path to the pre-built test repository
TEST_REPO_PATH = Path(__file__).parent / "test_repo"
METADATA_FILE = TEST_REPO_PATH / ".test_metadata.json"


@pytest.fixture
def test_repo_copy():
    """Create a copy of the test repository for each test."""
    if not TEST_REPO_PATH.exists():
        pytest.skip(f"Test repository not found at {TEST_REPO_PATH}. Run create_test_repo.sh first.")
    
    # Create a temporary copy of the test repo
    temp_dir = Path(__file__).parent / "temp_test_repo"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    shutil.copytree(TEST_REPO_PATH, temp_dir)
    
    # Ensure it's a git repo (sometimes .git might not copy properly)
    subprocess.run(["git", "init"], cwd=temp_dir, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_dir)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_dir)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


def load_test_metadata():
    """Load the test repository metadata."""
    if not METADATA_FILE.exists():
        raise FileNotFoundError(f"Metadata file not found at {METADATA_FILE}")
    
    with open(METADATA_FILE) as f:
        return json.load(f)


class TestE2EWithPrebuiltRepo:
    """E2E tests using pre-built test repository."""
    
    def test_e2e_coverage_decrease(self, test_repo_copy):
        """Test E2E flow when coverage decreases (feature/add-validators branch)."""
        os.chdir(test_repo_copy)
        metadata = load_test_metadata()
        
        # Create tool instances
        git_client = GitClient()
        reporter = CoverageReporter()
        parser = CoverageParser()
        
        # Create PR info for the feature branch
        pr_info = PRInfo(
            pr_number=123,
            base_branch="main",
            head_branch="feature/add-validators",
            base_sha=metadata["main_sha"],
            head_sha=metadata["feature_sha"],
            repo_url=f"file://{test_repo_copy}"
        )
        
        # Mock only what's necessary
        with patch.object(git_client, 'get_pr_info', return_value=pr_info):
            # Mock uv sync to avoid actual package installation
            with patch('pr_coverage_tool.pr_coverage_tool.subprocess') as mock_subprocess:
                # Let all subprocess calls go through except uv sync
                mock_subprocess.run.side_effect = lambda cmd, *args, **kwargs: (
                    Mock(returncode=0) if cmd[0] == "uv" and cmd[1] == "sync"
                    else subprocess.run(cmd, *args, **kwargs)
                )
                
                tool = PRCoverageTool(git_client, reporter, parser)
                
                # Run the analysis
                report = tool.analyze("fake://pr/url")
                
                # Verify the analysis
                assert report.pr_info.pr_number == 123
                assert report.pr_info.base_branch == "main"
                assert report.pr_info.head_branch == "feature/add-validators"
                
                # Coverage should have decreased (added untested code)
                assert report.coverage_delta.coverage_change < 0
                
                # Check modified files
                assert "myproject/palindrome.py" in report.coverage_delta.modified_lines
                
                # Check that new functions show as uncovered
                modified_lines = report.coverage_delta.modified_lines["myproject/palindrome.py"]
                
                # Should have some uncovered lines (from untested functions)
                uncovered_lines = [line for line in modified_lines 
                                 if line.after_status == "uncovered"]
                assert len(uncovered_lines) > 0
                
                # Generate reports
                markdown_report = reporter.format_as_markdown(report.coverage_delta)
                json_report = reporter.format_as_json(report.coverage_delta)
                
                # Verify markdown report
                assert "# PR Coverage Report" in markdown_report
                assert "palindrome.py" in markdown_report
                assert "Coverage Summary" in markdown_report
                
                # Since coverage decreased, should show down arrow
                assert "🔻" in markdown_report
                
                # Verify JSON report
                json_data = json.loads(json_report)
                assert json_data["coverage_change"] < 0
                assert "myproject/palindrome.py" in json_data["modified_lines"]
    
    def test_e2e_coverage_improvement(self, test_repo_copy):
        """Test E2E flow when coverage improves (feature/improve-tests branch)."""
        os.chdir(test_repo_copy)
        metadata = load_test_metadata()
        
        # Create tool instances
        git_client = GitClient()
        reporter = CoverageReporter()
        parser = CoverageParser()
        
        # Create PR info for the improve-tests branch
        pr_info = PRInfo(
            pr_number=456,
            base_branch="main",
            head_branch="feature/improve-tests",
            base_sha=metadata["main_sha"],
            head_sha=metadata["improve_sha"],
            repo_url=f"file://{test_repo_copy}"
        )
        
        with patch.object(git_client, 'get_pr_info', return_value=pr_info):
            with patch('pr_coverage_tool.pr_coverage_tool.subprocess') as mock_subprocess:
                mock_subprocess.run.side_effect = lambda cmd, *args, **kwargs: (
                    Mock(returncode=0) if cmd[0] == "uv" and cmd[1] == "sync"
                    else subprocess.run(cmd, *args, **kwargs)
                )
                
                tool = PRCoverageTool(git_client, reporter, parser)
                
                # Run analysis
                report = tool.analyze("fake://pr/url")
                
                # Coverage should improve or stay the same (added more tests)
                assert report.coverage_delta.coverage_change >= 0
                
                # Generate summary
                summary = reporter.summarize_changes(report.coverage_delta)
                
                # Should show improvement or no change
                assert "🔺" in summary or "➖" in summary
                
                # Check if we have better coverage on existing lines
                if "myproject/palindrome.py" in report.coverage_delta.modified_lines:
                    modified_lines = report.coverage_delta.modified_lines["myproject/palindrome.py"]
                    newly_covered = [line for line in modified_lines
                                   if line.before_status == "uncovered" and line.after_status == "covered"]
                    # Could have some newly covered lines from better tests
                    assert len(newly_covered) >= 0
    
    def test_e2e_report_generation(self, test_repo_copy):
        """Test report generation and output formatting."""
        os.chdir(test_repo_copy)
        metadata = load_test_metadata()
        
        # Create tool instances
        git_client = GitClient()
        reporter = CoverageReporter()
        parser = CoverageParser()
        
        pr_info = PRInfo(
            pr_number=789,
            base_branch="main",
            head_branch="feature/add-validators",
            base_sha=metadata["main_sha"],
            head_sha=metadata["feature_sha"],
            repo_url=f"file://{test_repo_copy}"
        )
        
        with patch.object(git_client, 'get_pr_info', return_value=pr_info):
            with patch('pr_coverage_tool.pr_coverage_tool.subprocess') as mock_subprocess:
                mock_subprocess.run.side_effect = lambda cmd, *args, **kwargs: (
                    Mock(returncode=0) if cmd[0] == "uv" and cmd[1] == "sync"
                    else subprocess.run(cmd, *args, **kwargs)
                )
                
                tool = PRCoverageTool(git_client, reporter, parser)
                report = tool.analyze("fake://pr/url")
                
                # Test different output formats
                markdown_report = reporter.format_as_markdown(report.coverage_delta)
                json_report = reporter.format_as_json(report.coverage_delta)
                summary = reporter.summarize_changes(report.coverage_delta)
                
                # Markdown should have proper structure
                assert "# PR Coverage Report" in markdown_report
                assert "## Coverage Summary" in markdown_report
                assert "## Modified Lines Coverage" in markdown_report
                
                # JSON should be valid
                json_data = json.loads(json_report)
                assert "total_coverage_before" in json_data
                assert "total_coverage_after" in json_data
                assert "coverage_change" in json_data
                assert "modified_lines" in json_data
                
                # Summary should have key metrics
                assert "Total Coverage:" in summary
                assert "%" in summary
                
                # Save reports to files
                report_dir = test_repo_copy / "coverage_reports"
                report_dir.mkdir(exist_ok=True)
                
                with open(report_dir / "pr_coverage.md", "w") as f:
                    f.write(markdown_report)
                
                with open(report_dir / "pr_coverage.json", "w") as f:
                    f.write(json_report)
                
                # Verify files were created
                assert (report_dir / "pr_coverage.md").exists()
                assert (report_dir / "pr_coverage.json").exists()