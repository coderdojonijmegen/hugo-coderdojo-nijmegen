from publisher.git import git


def test_git():
    ret, out, err = git("status")
    assert ret == 0
