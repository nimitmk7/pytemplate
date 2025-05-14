"""CLI module for PR coverage tool."""

import argparse
import sys
import os
import tempfile
import subprocess


def main() -> None:
    """Execute the PR coverage tool CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze code coverage changes in a pull request"
    )

    parser.add_argument(
        "pr_url",
        help="URL of the pull request to analyze (e.g., https://github.com/owner/repo/pull/123)"
    )

    parser.add_argument(
        "--format",
        choices=["markdown", "json", "summary"],
        default="markdown",
        help="Output format for the report"
    )

    parser.add_argument(
        "--output", "-o",
        help="File path to write the output (default: stdout)"
    )

    args = parser.parse_args()

    print("Starting PR Coverage Tool")
    print(f"PR URL: {args.pr_url}")
    print(f"Output format: {args.format}")

    # Store the original working directory for output file
    original_cwd = os.getcwd()
    
    # If output path is specified and relative, convert to absolute path
    output_path = None
    if args.output:
        output_path = os.path.abspath(args.output)
        print(f"Output will be saved to: {output_path}")

    # Derive the repository URL for cloning
    repo_clone_url = args.pr_url.split("/pull/")[0]
    print(f"Cloning repository: {repo_clone_url}")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Clone the repository into a temporary directory
            subprocess.run(
                ["git", "clone", repo_clone_url, tmpdir],
                check=True,
                capture_output=True
            )
            os.chdir(tmpdir)
            print(f"Repository cloned to {tmpdir}")

            # Import tool components after switching directory
            from .pr_coverage_tool import PRCoverageTool
            from .git_client import GitClient
            from .coverage_reporter import CoverageReporter
            from .coverage_parser import CoverageParser

            print("Initializing components...")
            git_client = GitClient()
            reporter = CoverageReporter()
            parser_instance = CoverageParser()
            tool = PRCoverageTool(git_client, reporter, parser_instance)

            print("Analyzing pull request...")
            report = tool.analyze(args.pr_url)

            if report is None or report.coverage_delta is None:
                print("No coverage data found or analysis returned no results.")
                return

            # Generate output based on the selected format
            if args.format == "json":
                output = reporter.format_as_json(report.coverage_delta)
            elif args.format == "summary":
                output = reporter.summarize_changes(report.coverage_delta)
            else:
                output = reporter.format_as_markdown(report.coverage_delta)

            if not output.strip():
                print("No coverage changes to report.")
                return

            # Write to file or print to stdout
            if output_path:
                with open(output_path, "w") as f:
                    f.write(output)
                print(f"Report written to {output_path}")
            else:
                print("Coverage Report:")
                print(output)

    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()