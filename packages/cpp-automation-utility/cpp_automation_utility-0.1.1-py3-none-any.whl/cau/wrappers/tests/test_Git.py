"""Tests for Git module."""
import pytest

from cau.wrappers.Git import DiffCollection, Git

@pytest.mark.usefixtures("mock_repo")
class TestGit:
    """Tests for git wrapper class."""
    git_wrapper = None

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Setup of test fixtures."""
        self.git_wrapper = Git()

    def test_changed_files(self, changed_files: DiffCollection) -> None:
        """
        Asserts changed files returns correct file commits.

        Args:
            changed_files (DiffCollection): expected file commits
        """
        self.git_wrapper = Git()
        expected = changed_files
        expected.sort(key=lambda d: d.a_path)
        result = self.git_wrapper.changed_files()
        result.sort(key=lambda d: d.a_path)
        assert result == expected
