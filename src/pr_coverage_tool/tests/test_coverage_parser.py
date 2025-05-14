"""Unit tests for the Coverage Parser."""
import tempfile
from pathlib import Path
import pytest

from pr_coverage_tool.coverage_parser import CoverageParser
from pr_coverage_tool.coverage_parser_interface import (
    CoverageData,
    FileCoverage,
)


class TestCoverageParser:
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = CoverageParser()

    def test_parse_simple_coverage_xml(self) -> None:
        """Test parsing a simple coverage XML file."""
        xml_content = """<?xml version="1.0" ?>
<coverage line-rate="0.85">
    <packages>
        <package>
            <classes>
                <class filename="test.py">
                    <lines>
                        <line number="1" hits="1"/>
                        <line number="2" hits="0"/>
                        <line number="3" hits="2"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
            tmp.write(xml_content)
            tmp.flush()
            
            self.parser.set_commit_sha("abc123")
            result = self.parser.parse_coverage_xml(tmp.name)
            
            Path(tmp.name).unlink()
        
        assert result.commit_sha == "abc123"
        assert result.total_coverage == 85.0
        assert "test.py" in result.files
        assert result.files["test.py"].total_lines == 3
        assert result.files["test.py"].covered_lines == 2
        assert result.files["test.py"].coverage_percentage == pytest.approx(66.67, rel=0.01)
        assert result.files["test.py"].line_data[1] == "covered"
        assert result.files["test.py"].line_data[2] == "uncovered"
        assert result.files["test.py"].line_data[3] == "covered"

    def test_parse_multi_file_coverage(self) -> None:
        """Test parsing coverage with multiple files."""
        xml_content = """<?xml version="1.0" ?>
<coverage line-rate="0.75">
    <packages>
        <package>
            <classes>
                <class filename="file1.py">
                    <lines>
                        <line number="1" hits="1"/>
                        <line number="2" hits="0"/>
                    </lines>
                </class>
                <class filename="file2.py">
                    <lines>
                        <line number="1" hits="3"/>
                        <line number="2" hits="1"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
            tmp.write(xml_content)
            tmp.flush()
            
            self.parser.set_commit_sha("def456")
            result = self.parser.parse_coverage_xml(tmp.name)
            
            Path(tmp.name).unlink()
        
        assert result.total_coverage == 75.0
        assert len(result.files) == 2
        assert "file1.py" in result.files
        assert "file2.py" in result.files
        assert result.files["file1.py"].covered_lines == 1
        assert result.files["file2.py"].covered_lines == 2

    def test_parse_empty_coverage(self) -> None:
        """Test parsing coverage with no lines."""
        xml_content = """<?xml version="1.0" ?>
<coverage line-rate="0.0">
    <packages>
        <package>
            <classes>
                <class filename="empty.py">
                    <lines>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
            tmp.write(xml_content)
            tmp.flush()
            
            result = self.parser.parse_coverage_xml(tmp.name)
            
            Path(tmp.name).unlink()
        
        assert result.total_coverage == 0.0
        assert "empty.py" in result.files
        assert result.files["empty.py"].total_lines == 0
        assert result.files["empty.py"].covered_lines == 0
        assert result.files["empty.py"].coverage_percentage == 0.0