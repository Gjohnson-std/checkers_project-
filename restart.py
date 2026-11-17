class RestartVote:
    """Track confirmation from the requester and the opponent's vote."""

    def __init__(self):
        self.stage = None

    def request(self):
        if self.stage is None:
            self.stage = "confirm"

    def cancel(self):
        self.stage = None

    def confirm(self, accepted):
        if self.stage != "confirm":
            return
        self.stage = "vote" if accepted else None

    def vote(self, accepted):
        if self.stage != "vote":
            return False
        self.stage = None
        return accepted
