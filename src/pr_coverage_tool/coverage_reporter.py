"""Implementation of the Coverage Reporter."""
import json

from .coverage_reporter_interface import CoverageReporterInterface
from .pr_coverage_tool_interface import CoverageDelta, LineCoverage


class CoverageReporter(CoverageReporterInterface):
    """Concrete implementation of coverage reporting."""
    
    def generate_report(self, delta: CoverageDelta) -> str:
        """Generate a complete coverage report."""
        lines = [
            "# PR Coverage Report",
            "",
            self.summarize_changes(delta),
            "",
            "## Modified Lines Coverage",
            ""
        ]
        
        for file, line_coverage in delta.modified_lines.items():
            if line_coverage:
                lines.append(f"### {file}")
                lines.append(self.format_line_coverage(file, line_coverage))
                lines.append("")
        
        if delta.files_added:
            lines.extend([
                "## New Files",
                "",
                *[f"- {file}" for file in delta.files_added],
                ""
            ])
        
        if delta.files_removed:
            lines.extend([
                "## Removed Files",
                "",
                *[f"- {file}" for file in delta.files_removed],
                ""
            ])
        
        return "\n".join(lines)
    
    def format_line_coverage(self, file: str, lines: list[LineCoverage]) -> str:
        """Format line-by-line coverage changes."""
        rows = []
        
        # Group consecutive lines for better readability
        grouped_lines: list[list[LineCoverage]] = []
        current_group: list[LineCoverage] = []
        
        for line in sorted(lines, key=lambda x: x.line_number):
            if (not current_group or 
                line.line_number == current_group[-1].line_number + 1):
                current_group.append(line)
            else:
                grouped_lines.append(current_group)
                current_group = [line]
        
        if current_group:
            grouped_lines.append(current_group)
        
        for group in grouped_lines:
            if len(group) == 1:
                line = group[0]
                status_change = self._format_status_change(
                    line.before_status, line.after_status
                )
                rows.append(f"Line {line.line_number}: {status_change}")
            else:
                first_line = group[0].line_number
                last_line = group[-1].line_number
                
                # Check if all lines in group have same status change
                same_change = all(
                    self._format_status_change(line.before_status, line.after_status) ==
                    self._format_status_change(
                        group[0].before_status, group[0].after_status
                    )
                    for line in group
                )
                
                if same_change:
                    status_change = self._format_status_change(
                        group[0].before_status, group[0].after_status
                    )
                    rows.append(f"Lines {first_line}-{last_line}: {status_change}")
                else:
                    for line in group:
                        status_change = self._format_status_change(
                            line.before_status, line.after_status
                        )
                        rows.append(f"Line {line.line_number}: {status_change}")
        
        return "\n".join(rows)
    
    def summarize_changes(self, delta: CoverageDelta) -> str:
        """Generate a summary of coverage changes."""
        coverage_symbol = ("🔺" if delta.coverage_change > 0 
                          else "🔻" if delta.coverage_change < 0 
                          else "➖")
        
        summary = [
            "## Coverage Summary",
            "",
            (f"**Total Coverage:** {delta.total_coverage_before:.2f}% → "
             f"{delta.total_coverage_after:.2f}% ({delta.coverage_change:+.2f}%) "
             f"{coverage_symbol}"),
            ""
        ]
        
        # Count line coverage changes
        lines_improved = 0
        lines_degraded = 0
        
        for file_lines in delta.modified_lines.values():
            for line in file_lines:
                if line.before_status == 'uncovered' and line.after_status == 'covered':
                    lines_improved += 1
                elif (line.before_status == 'covered' and 
                      line.after_status == 'uncovered'):
                    lines_degraded += 1
        
        if lines_improved > 0:
            summary.append(f"✅ {lines_improved} line(s) newly covered")
        if lines_degraded > 0:
            summary.append(f"❌ {lines_degraded} line(s) lost coverage")
        
        if delta.files_added:
            summary.append(f"📄 {len(delta.files_added)} new file(s)")
        if delta.files_removed:
            summary.append(f"🗑️ {len(delta.files_removed)} file(s) removed")
        
        return "\n".join(summary)
    
    def format_as_markdown(self, delta: CoverageDelta) -> str:
        """Format the report as markdown for PR comments."""
        return self.generate_report(delta)
    
    def format_as_json(self, delta: CoverageDelta) -> str:
        """Format the report as JSON for API responses."""
        data: dict[str, object] = {
            "total_coverage_before": delta.total_coverage_before,
            "total_coverage_after": delta.total_coverage_after,
            "coverage_change": delta.coverage_change,
            "modified_lines": {},
            "files_added": delta.files_added,
            "files_removed": delta.files_removed
        }
        
        modified_lines_data: dict[str, list[dict[str, object]]] = {}
        for file, lines in delta.modified_lines.items():
            modified_lines_data[file] = [
                {
                    "line_number": line.line_number,
                    "before_status": line.before_status,
                    "after_status": line.after_status
                }
                for line in lines
            ]
        data["modified_lines"] = modified_lines_data
        
        return json.dumps(data, indent=2)
    
    def _format_status_change(self, before: str, after: str) -> str:
        """Format the status change for a line."""
        if before == after:
            return f"{before} (no change)"
        
        if before == 'not_present' and after != 'not_present':
            return f"newly added - {after}"
        elif before != 'not_present' and after == 'not_present':
            return f"removed (was {before})"
        elif before == 'uncovered' and after == 'covered':
            return "✅ now covered"
        elif before == 'covered' and after == 'uncovered':
            return "❌ lost coverage"
        else:
            return f"{before} → {after}"