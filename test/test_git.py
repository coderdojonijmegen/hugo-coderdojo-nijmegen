from publisher.git import git


def test_git():
    ret, out, err = git(f"status")
    assert ret == 0
