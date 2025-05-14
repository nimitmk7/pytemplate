"""Implementation of the Git Client."""
import re
import subprocess
from typing import Dict, List
from urllib.parse import urlparse

from .git_client_interface import GitClientInterface
from .pr_coverage_tool_interface import PRInfo


class GitClient(GitClientInterface):
    """Concrete implementation of git operations."""
    
    def checkout(self, commit: str) -> None:
        """Checkout a specific commit."""
        subprocess.run(["git", "checkout", commit], check=True, capture_output=True)
    
    def get_pr_info(self, pr_url: str) -> PRInfo:
        """Extract PR information from URL."""
        # Parse GitHub/GitLab PR URL
        # Example: https://github.com/owner/repo/pull/123
        parsed = urlparse(pr_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if 'github.com' in parsed.netloc:
            # GitHub PR URL format
            if len(path_parts) >= 4 and path_parts[2] == 'pull':
                owner = path_parts[0]
                repo = path_parts[1]
                pr_number = int(path_parts[3])
                repo_url = f"https://github.com/{owner}/{repo}"
            else:
                raise ValueError(f"Invalid GitHub PR URL: {pr_url}")
        else:
            raise ValueError(f"Unsupported PR URL: {pr_url}")
        
        # Fetch PR information via git or API
        # For now, we'll get basic info from git
        # In production, this would use GitHub API
        
        # Get current branch info
        result = subprocess.run(
            ["git", "branch", "-r", "--contains", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # This is simplified - in production would use API
        head_branch = f"pr-{pr_number}"
        base_branch = "main"
        
        # # Get SHA for branches
        # head_sha = self._get_commit_sha(head_branch)
        # base_sha = self._get_commit_sha(base_branch)

        subprocess.run(
            ["git", "fetch", "origin", base_branch],
            check=True, capture_output=True
             )
        subprocess.run(
             ["git", "fetch", "origin", f"pull/{pr_number}/head:{head_branch}"],
             check=True, capture_output=True
             )
        
        head_sha = self._get_commit_sha(head_branch)
        base_sha = self._get_commit_sha(base_branch)
 
        
        return PRInfo(
            pr_number=pr_number,
            base_branch=base_branch,
            head_branch=head_branch,
            base_sha=base_sha,
            head_sha=head_sha,
            repo_url=repo_url
        )
    
    def get_modified_files(self, base: str, head: str) -> List[str]:
        """Get list of modified files between two commits."""
        result = subprocess.run(
            ["git", "diff", "--name-only", base, head],
            capture_output=True,
            text=True,
            check=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    
    def get_modified_lines(self, base: str, head: str, file: str) -> List[int]:
        """Get modified line numbers for a specific file."""
        result = subprocess.run(
            ["git", "diff", "-U0", base, head, "--", file],
            capture_output=True,
            text=True,
            check=True
        )
        
        modified_lines = []
        for line in result.stdout.split('\n'):
            # Parse unified diff format
            # Example: @@ -1,3 +1,5 @@
            match = re.match(r'@@ -\d+,?\d* \+(\d+),?(\d*) @@', line)
            if match:
                start_line = int(match.group(1))
                line_count = int(match.group(2) or 1)
                modified_lines.extend(range(start_line, start_line + line_count))
        
        return sorted(set(modified_lines))
    
    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    def stash_changes(self) -> None:
        """Stash any uncommitted changes."""
        subprocess.run(["git", "stash", "--include-untracked"], check=True)
    
    def pop_stash(self) -> None:
        """Restore previously stashed changes."""
        # Check if there's anything to pop
        result = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            subprocess.run(["git", "stash", "pop"], check=True)
    
    def _get_commit_sha(self, ref: str) -> str:
        """Get the SHA for a given reference."""
        result = subprocess.run(
            ["git", "rev-parse", ref],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()