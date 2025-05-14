"""Unit tests for the Git Client."""
import subprocess
from unittest.mock import Mock, patch
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import pytest

from pr_coverage_tool.git_client import GitClient
from pr_coverage_tool.pr_coverage_tool_interface import PRInfo


class TestGitClient:
    def setup_method(self):
        """Set up test fixtures."""
        self.client = GitClient()

    @patch('subprocess.run')
    def test_checkout(self, mock_run):
        """Test checking out a commit."""
        self.client.checkout("abc123")
        mock_run.assert_called_once_with(
            ["git", "checkout", "abc123"],
            check=True,
            capture_output=True
        )

    def test_get_pr_info_github(self):
        """Test extracting PR info from GitHub URL."""
        with patch.object(self.client, '_get_commit_sha') as mock_sha:
            mock_sha.side_effect = ["base_sha", "head_sha"]
            
            # Mock subprocess.run to avoid actual git commands
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(stdout="", returncode=0)
                
                pr_info = self.client.get_pr_info("https://github.com/owner/repo/pull/123")
                
                assert pr_info.pr_number == 123
                assert pr_info.repo_url == "https://github.com/owner/repo"
                assert pr_info.base_branch == "main"
                assert pr_info.head_branch == "pr-123"

    def test_get_pr_info_invalid_url(self):
        """Test handling invalid PR URL."""
        with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
            self.client.get_pr_info("https://github.com/owner/repo/issues/123")

    @patch('subprocess.run')
    def test_get_modified_files(self, mock_run):
        """Test getting modified files."""
        mock_run.return_value = Mock(
            stdout="file1.py\nfile2.py\n",
            returncode=0
        )
        
        files = self.client.get_modified_files("base", "head")
        
        assert files == ["file1.py", "file2.py"]
        mock_run.assert_called_once_with(
            ["git", "diff", "--name-only", "base", "head"],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_get_modified_lines(self, mock_run):
        """Test getting modified lines for a file."""
        # Mock git diff output
        diff_output = """
@@ -10,3 +10,5 @@
 unchanged line
-removed line
+added line 1
+added line 2
@@ -20,2 +22,4 @@
 another unchanged
+new line
+another new line
"""
        mock_run.return_value = Mock(stdout=diff_output, returncode=0)
        
        lines = self.client.get_modified_lines("base", "head", "file.py")
        
        # Lines 10-14 (first hunk) and 22-25 (second hunk)
        assert sorted(lines) == [10, 11, 12, 13, 14, 22, 23, 24, 25]

    @patch('subprocess.run')
    def test_get_current_branch(self, mock_run):
        """Test getting current branch name."""
        mock_run.return_value = Mock(stdout="feature-branch\n", returncode=0)
        
        branch = self.client.get_current_branch()
        
        assert branch == "feature-branch"
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_stash_changes(self, mock_run):
        """Test stashing changes."""
        self.client.stash_changes()
        
        mock_run.assert_called_once_with(
            ["git", "stash", "--include-untracked"],
            check=True
        )

    @patch('subprocess.run')
    def test_pop_stash_with_stash(self, mock_run):
        """Test popping stash when stash exists."""
        # First call returns stash list, second call pops
        mock_run.side_effect = [
            Mock(stdout="stash@{0}: WIP on main\n", returncode=0),
            Mock(returncode=0)
        ]
        
        self.client.pop_stash()
        
        assert mock_run.call_count == 2
        mock_run.assert_any_call(["git", "stash", "list"], capture_output=True, text=True)
        mock_run.assert_any_call(["git", "stash", "pop"], check=True)

    @patch('subprocess.run')
    def test_pop_stash_no_stash(self, mock_run):
        """Test popping stash when no stash exists."""
        mock_run.return_value = Mock(stdout="", returncode=0)
        
        self.client.pop_stash()
        
        # Should only call stash list, not pop
        mock_run.assert_called_once_with(
            ["git", "stash", "list"],
            capture_output=True,
            text=True
        )