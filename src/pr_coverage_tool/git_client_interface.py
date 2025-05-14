"""
Git client interface module.
Handles git operations for checking out commits and getting PR information.
"""
from abc import ABC, abstractmethod
from .pr_coverage_tool_interface import PRInfo


class GitClientInterface(ABC):
    """Defines the interface for git operations."""

    @abstractmethod
    def checkout(self, commit: str) -> None:
        """Checkout a specific commit.
        
        Args:
            commit: SHA of the commit to checkout
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_pr_info(self, pr_url: str) -> PRInfo:
        """Extract PR information from URL.
        
        Args:
            pr_url: URL of the pull request
            
        Returns:
            PRInfo object with PR details
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_modified_files(self, base: str, head: str) -> list[str]:
        """Get list of modified files between two commits.
        
        Args:
            base: Base commit SHA
            head: Head commit SHA
            
        Returns:
            List of modified file paths
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_modified_lines(self, base: str, head: str, file: str) -> list[int]:
        """Get modified line numbers for a specific file.
        
        Args:
            base: Base commit SHA
            head: Head commit SHA
            file: File path to analyze
            
        Returns:
            List of modified line numbers
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_current_branch(self) -> str:
        """Get the name of the current branch.
        
        Returns:
            Current branch name
        """
        pass  # pragma: no cover

    @abstractmethod
    def stash_changes(self) -> None:
        """Stash any uncommitted changes."""
        pass  # pragma: no cover

    @abstractmethod
    def pop_stash(self) -> None:
        """Restore previously stashed changes."""
        pass  # pragma: no cover