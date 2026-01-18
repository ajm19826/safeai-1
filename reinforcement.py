class Reinforcement:
    def __init__(self):
        self.rewards = 0

    def reward(self):
        self.rewards += 1

    def punish(self):
        self.rewards -= 1
