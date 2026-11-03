"""An extracted release must not be attributed to an unrelated enclosing repo."""

import subprocess

from robustcluster_abeta.manifest import Run, git_metadata


def test_archive_does_not_inherit_parent_git_commit(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
         "commit", "--allow-empty", "-qm", "Unrelated parent repository"],
        cwd=tmp_path, check=True,
    )
    assert git_metadata(tmp_path)["git_commit"]
    archive = tmp_path / "extracted-source"
    archive.mkdir()
    run = Run({"project_root": str(archive), "inputs": {}}, "synthetic-test")
    assert run.data["git_commit"] is None
    assert run.data["git_dirty"] is None
    run.finish("SUCCESS")
