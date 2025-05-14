"""Unit tests for the Coverage Reporter."""
import json
import pytest

from pr_coverage_tool.coverage_reporter import CoverageReporter
from pr_coverage_tool.pr_coverage_tool_interface import (
    CoverageDelta,
    LineCoverage,
)


class TestCoverageReporter:
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.reporter = CoverageReporter()

    def test_format_status_change(self) -> None:
        """Test formatting of status changes."""
        assert self.reporter._format_status_change("covered", "covered") == "covered (no change)"
        assert self.reporter._format_status_change("uncovered", "covered") == "✅ now covered"
        assert self.reporter._format_status_change("covered", "uncovered") == "❌ lost coverage"
        assert self.reporter._format_status_change("not_present", "covered") == "newly added - covered"
        assert self.reporter._format_status_change("covered", "not_present") == "removed (was covered)"

    def test_format_line_coverage_single_line(self) -> None:
        """Test formatting single line coverage."""
        lines = [
            LineCoverage(line_number=10, before_status="uncovered", after_status="covered"),
        ]
        
        result = self.reporter.format_line_coverage("test.py", lines)
        
        assert "Line 10: ✅ now covered" in result

    def test_format_line_coverage_consecutive_lines_same_change(self) -> None:
        """Test formatting consecutive lines with same change."""
        lines = [
            LineCoverage(line_number=10, before_status="uncovered", after_status="covered"),
            LineCoverage(line_number=11, before_status="uncovered", after_status="covered"),
            LineCoverage(line_number=12, before_status="uncovered", after_status="covered"),
        ]
        
        result = self.reporter.format_line_coverage("test.py", lines)
        
        assert "Lines 10-12: ✅ now covered" in result

    def test_format_line_coverage_mixed_changes(self) -> None:
        """Test formatting lines with different changes."""
        lines = [
            LineCoverage(line_number=10, before_status="uncovered", after_status="covered"),
            LineCoverage(line_number=11, before_status="covered", after_status="uncovered"),
            LineCoverage(line_number=12, before_status="uncovered", after_status="covered"),
        ]
        
        result = self.reporter.format_line_coverage("test.py", lines)
        lines_result = result.split('\n')
        
        assert "Line 10: ✅ now covered" in lines_result[0]
        assert "Line 11: ❌ lost coverage" in lines_result[1]
        assert "Line 12: ✅ now covered" in lines_result[2]

    def test_summarize_changes_improved(self) -> None:
        """Test summary when coverage improves."""
        delta = CoverageDelta(
            total_coverage_before=80.0,
            total_coverage_after=85.0,
            coverage_change=5.0,
            modified_lines={
                "test.py": [
                    LineCoverage(10, "uncovered", "covered"),
                    LineCoverage(11, "uncovered", "covered"),
                ]
            },
            files_added=["new_file.py"],
            files_removed=[]
        )
        
        summary = self.reporter.summarize_changes(delta)
        
        assert "80.00% → 85.00% (+5.00%) 🔺" in summary
        assert "✅ 2 line(s) newly covered" in summary
        assert "📄 1 new file(s)" in summary

    def test_summarize_changes_degraded(self) -> None:
        """Test summary when coverage degrades."""
        delta = CoverageDelta(
            total_coverage_before=85.0,
            total_coverage_after=80.0,
            coverage_change=-5.0,
            modified_lines={
                "test.py": [
                    LineCoverage(10, "covered", "uncovered"),
                ]
            },
            files_added=[],
            files_removed=["old_file.py"]
        )
        
        summary = self.reporter.summarize_changes(delta)
        
        assert "85.00% → 80.00% (-5.00%) 🔻" in summary
        assert "❌ 1 line(s) lost coverage" in summary
        assert "🗑️ 1 file(s) removed" in summary

    def test_generate_report(self) -> None:
        """Test full report generation."""
        delta = CoverageDelta(
            total_coverage_before=80.0,
            total_coverage_after=85.0,
            coverage_change=5.0,
            modified_lines={
                "test.py": [
                    LineCoverage(10, "uncovered", "covered"),
                ]
            },
            files_added=["new.py"],
            files_removed=["old.py"]
        )
        
        report = self.reporter.generate_report(delta)
        
        assert "# PR Coverage Report" in report
        assert "## Coverage Summary" in report
        assert "## Modified Lines Coverage" in report
        assert "### test.py" in report
        assert "## New Files" in report
        assert "## Removed Files" in report

    def test_format_as_json(self) -> None:
        """Test JSON formatting."""
        delta = CoverageDelta(
            total_coverage_before=80.0,
            total_coverage_after=85.0,
            coverage_change=5.0,
            modified_lines={
                "test.py": [
                    LineCoverage(10, "uncovered", "covered"),
                ]
            },
            files_added=["new.py"],
            files_removed=["old.py"]
        )
        
        json_output = self.reporter.format_as_json(delta)
        data = json.loads(json_output)
        
        assert data["total_coverage_before"] == 80.0
        assert data["total_coverage_after"] == 85.0
        assert data["coverage_change"] == 5.0
        assert len(data["modified_lines"]["test.py"]) == 1
        assert data["files_added"] == ["new.py"]
        assert data["files_removed"] == ["old.py"]