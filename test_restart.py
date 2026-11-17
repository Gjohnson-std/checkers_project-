from restart import RestartVote


def test_restart_requires_requester_confirmation_and_opponent_vote():
    restart = RestartVote()

    restart.request()
    assert restart.stage == "confirm"

    restart.confirm(True)
    assert restart.stage == "vote"

    assert restart.vote(True)
    assert restart.stage is None


def test_declining_confirmation_cancels_restart():
    restart = RestartVote()

    restart.request()
    restart.confirm(False)

    assert restart.stage is None
    assert not restart.vote(True)


def test_opponent_declining_vote_cancels_restart():
    restart = RestartVote()

    restart.request()
    restart.confirm(True)

    assert not restart.vote(False)
    assert restart.stage is None
