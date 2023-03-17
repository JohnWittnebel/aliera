# this keeps track of the results of a tournament

class TourData():
    def __init__(self, size):
        self.p1Wins = []
        self.p2Wins = []
        for _ in range(size):
            self.p1Wins.append(0)
        for _ in range(size):
            self.p2Wins.append(0)
