"""Git wrapper around git commands."""
import logging
import pathlib

import attrs
import git

DiffCollection = list[git.Diff]

logger = logging.getLogger("CAU")

#pylint: disable=too-few-public-methods
@attrs.define()
class Git:
    """Git wrapper class around commands to work with repository."""
    main_branch: pathlib.Path = attrs.field(
        factory=lambda: pathlib.Path("origin")/"main",
        converter=pathlib.Path,
        validator=attrs.validators.instance_of(pathlib.Path),
    )
    _repo = attrs.field(factory=lambda: git.Repo(pathlib.Path.cwd()), init=False, repr=False, eq=False)

    def changed_files(self) -> DiffCollection:
        """
        Interrogates git to get a list of changed files between working directory and the remote main line branch.

        Returns:
            DiffCollection: changed file commits
        """
        remote: git.Remote = self._repo.remote(name=str(self.main_branch.parent))
        main: git.RemoteReference = next(ref for ref in remote.refs if str(self.main_branch) == ref.name)
        remote_head: git.Commit = self._repo.rev_parse(main.name)
        logger.debug("Mainline: %s", main.name)
        logger.debug("Remote head: %s", remote_head)
        return list(set(remote_head.diff("HEAD") + self._repo.index.diff("HEAD") + self._repo.index.diff(None)))
