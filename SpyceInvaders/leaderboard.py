import os.path

from SpyceInvaders import settings


class Leaderboard:

    def __init__(self):
        self.file_path = os.path.join(settings.DATA_PATH, "leaderboard")

    def read_from_file(self):
        with open(self.file_path, "r") as file:
            return file.readlines()

    def write_to_file(self, name, score):
        board = []
        for line in self.read_from_file():
            tmp = line.split()
            board.append((tmp[0], int(tmp[1])))
        board.append((name, score))
        board.sort(key=lambda tup: tup[1], reverse=True)
        with open(self.file_path, "w") as file:
            for i in range(min(len(board), settings.LEADERBOARD_LENGTH)):
                file.write("{} {}\n".format(board[i][0], str(board[i][1])))
