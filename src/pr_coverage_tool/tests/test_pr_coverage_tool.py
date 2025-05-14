"""Unit tests for the PR Coverage Tool."""
from unittest.mock import Mock, patch
import pytest

from pr_coverage_tool.pr_coverage_tool import PRCoverageTool
from pr_coverage_tool.pr_coverage_tool_interface import (
    CoverageDelta,
    CoverageReport,
    LineCoverage,
    PRInfo,
)
from pr_coverage_tool.coverage_parser_interface import (
    CoverageData,
    FileCoverage,
)


class TestPRCoverageTool:
    def setup_method(self):
        """Set up test fixtures."""
        self.git_client = Mock()
        self.reporter = Mock()
        self.coverage_parser = Mock()
        self.tool = PRCoverageTool(self.git_client, self.reporter, self.coverage_parser)

    def test_analyze_full_flow(self):
        """Test the full analyze flow."""
        # Setup PR info
        pr_info = PRInfo(
            pr_number=123,
            base_branch="main",
            head_branch="feature",
            base_sha="base123",
            head_sha="head456",
            repo_url="https://github.com/test/repo"
        )
        self.git_client.get_pr_info.return_value = pr_info
        self.git_client.get_current_branch.return_value = "current"
        
        # Setup merge base
        with patch.object(self.tool, 'get_merge_base', return_value="merge123"):
            # Setup modified files
            self.git_client.get_modified_files.return_value = ["file1.py"]
            self.git_client.get_modified_lines.return_value = [10, 11, 12]
            
            # Setup coverage data
            before_coverage = CoverageData(
                commit_sha="merge123",
                total_coverage=80.0,
                files={
                    "file1.py": FileCoverage(
                        filename="file1.py",
                        total_lines=100,
                        covered_lines=80,
                        coverage_percentage=80.0,
                        line_data={10: "uncovered", 11: "covered", 12: "uncovered"}
                    )
                }
            )
            
            after_coverage = CoverageData(
                commit_sha="head456",
                total_coverage=85.0,
                files={
                    "file1.py": FileCoverage(
                        filename="file1.py",
                        total_lines=100,
                        covered_lines=85,
                        coverage_percentage=85.0,
                        line_data={10: "covered", 11: "covered", 12: "covered"}
                    )
                }
            )
            
            with patch.object(self.tool, 'compute_coverage') as mock_compute:
                mock_compute.side_effect = [before_coverage, after_coverage]
                
                # Setup comparison
                expected_delta = CoverageDelta(
                    total_coverage_before=80.0,
                    total_coverage_after=85.0,
                    coverage_change=5.0,
                    modified_lines={
                        "file1.py": [
                            LineCoverage(10, "uncovered", "covered"),
                            LineCoverage(11, "covered", "covered"),
                            LineCoverage(12, "uncovered", "covered"),
                        ]
                    },
                    files_added=[],
                    files_removed=[]
                )
                
                with patch.object(self.tool, 'compare_coverage', return_value=expected_delta):
                    self.reporter.summarize_changes.return_value = "Coverage improved!"
                    
                    # Execute
                    report = self.tool.analyze("https://github.com/test/repo/pull/123")
                    
                    # Verify
                    assert report.pr_info == pr_info
                    assert report.coverage_delta == expected_delta
                    assert report.summary == "Coverage improved!"
                    
                    # Verify git operations
                    self.git_client.stash_changes.assert_called_once()
                    self.git_client.checkout.assert_any_call("merge123")
                    self.git_client.checkout.assert_any_call("head456")
                    self.git_client.checkout.assert_any_call("current")
                    self.git_client.pop_stash.assert_called_once()

    @patch('subprocess.run')
    def test_get_merge_base(self, mock_run):
        """Test getting merge base."""
        mock_run.return_value = Mock(stdout="merge123\n", returncode=0)
        
        result = self.tool.get_merge_base("main", "feature")
        
        assert result == "merge123"
        mock_run.assert_called_once_with(
            ["git", "merge-base", "main", "feature"],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    @patch('pathlib.Path.unlink')
    def test_compute_coverage(self, mock_unlink, mock_tempfile, mock_run):
        """Test computing coverage at a commit."""
        # Setup temporary file
        temp_file = Mock()
        temp_file.name = "/tmp/coverage.xml"
        mock_tempfile.return_value.__enter__.return_value = temp_file
        
        # Setup coverage parser mock
        expected_coverage = CoverageData(
            commit_sha="abc123",
            total_coverage=85.0,
            files={
                "test.py": FileCoverage(
                    filename="test.py",
                    total_lines=2,
                    covered_lines=1,
                    coverage_percentage=50.0,
                    line_data={1: "covered", 2: "uncovered"}
                )
            }
        )
        self.coverage_parser.parse_coverage_xml.return_value = expected_coverage
        
        # Execute
        result = self.tool.compute_coverage("abc123")
        
        # Verify
        self.coverage_parser.set_commit_sha.assert_called_once_with("abc123")
        self.coverage_parser.parse_coverage_xml.assert_called_once_with("/tmp/coverage.xml")
        assert result == expected_coverage

    def test_compare_coverage(self):
        """Test comparing coverage between commits."""
        before = CoverageData(
            commit_sha="before",
            total_coverage=80.0,
            files={
                "file1.py": FileCoverage(
                    filename="file1.py",
                    total_lines=100,
                    covered_lines=80,
                    coverage_percentage=80.0,
                    line_data={10: "uncovered", 11: "covered"}
                ),
                "removed.py": FileCoverage(
                    filename="removed.py",
                    total_lines=50,
                    covered_lines=40,
                    coverage_percentage=80.0,
                    line_data={}
                )
            }
        )
        
        after = CoverageData(
            commit_sha="after",
            total_coverage=85.0,
            files={
                "file1.py": FileCoverage(
                    filename="file1.py",
                    total_lines=100,
                    covered_lines=85,
                    coverage_percentage=85.0,
                    line_data={10: "covered", 11: "covered", 12: "covered"}
                ),
                "new.py": FileCoverage(
                    filename="new.py",
                    total_lines=20,
                    covered_lines=18,
                    coverage_percentage=90.0,
                    line_data={}
                )
            }
        )
        
        modified_lines = {
            "file1.py": [10, 12]
        }
        
        result = self.tool.compare_coverage(before, after, modified_lines)
        
        assert result.total_coverage_before == 80.0
        assert result.total_coverage_after == 85.0
        assert result.coverage_change == 5.0
        assert result.files_added == ["new.py"]
        assert result.files_removed == ["removed.py"]
        
        file1_lines = result.modified_lines["file1.py"]
        assert len(file1_lines) == 2
        
        line10 = next(l for l in file1_lines if l.line_number == 10)
        assert line10.before_status == "uncovered"
        assert line10.after_status == "covered"
        
        line12 = next(l for l in file1_lines if l.line_number == 12)
        assert line12.before_status == "not_present"
        assert line12.after_status == "covered"