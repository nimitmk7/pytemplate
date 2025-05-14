"""Implementation of the Coverage Parser."""
from pathlib import Path
from xml.etree import ElementTree

from .coverage_parser_interface import (
    CoverageData,
    CoverageParserInterface,
    FileCoverage,
)


class CoverageParser(CoverageParserInterface):
    """Concrete implementation of coverage data parsing."""
    
    def __init__(self):
        """Initialize the parser."""
        self._commit_sha = ""
    
    def set_commit_sha(self, commit_sha: str) -> None:
        """Set the commit SHA for the coverage data."""
        self._commit_sha = commit_sha
    
    def parse_coverage_xml(self, xml_path: str) -> CoverageData:
        """Parse coverage data from XML file."""
        tree = ElementTree.parse(xml_path)
        root = tree.getroot()
        
        total_coverage = float(root.attrib.get('line-rate', 0)) * 100
        
        files = {}
        for package in root.findall('.//package'):
            for class_elem in package.findall('./classes/class'):
                filename = class_elem.attrib['filename']
                
                lines = class_elem.findall('./lines/line')
                total_lines = len(lines)
                covered_lines = sum(1 for line in lines if line.attrib.get('hits', '0') != '0')
                
                line_data = {}
                for line in lines:
                    line_num = int(line.attrib['number'])
                    hits = int(line.attrib.get('hits', 0))
                    line_data[line_num] = 'covered' if hits > 0 else 'uncovered'
                
                coverage_percentage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
                
                files[filename] = FileCoverage(
                    filename=filename,
                    total_lines=total_lines,
                    covered_lines=covered_lines,
                    coverage_percentage=coverage_percentage,
                    line_data=line_data
                )
        
        return CoverageData(
            commit_sha=self._commit_sha,
            total_coverage=total_coverage,
            files=files
        )