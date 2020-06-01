"""Defines Leaderboard class that handles game score."""

import os.path

from spyce_invaders import settings


class Leaderboard:
    """Creates filepath to leaderboard in data directory."""

    def __init__(self):
        self.file_path = os.path.join(settings.DATA_PATH, "leaderboard")

    def read_from_file(self):
        """Reads all lines from file and returns them."""
        try:
            file = open(self.file_path, "r")
            return file.readlines()
        except FileNotFoundError:
            return []

    def write_to_file(self, name, score):
        """Appends given name and score. Sorts leaderboard and writes to file.
        Writes up to the number of entries specified in settings module."""
        board = []
        for line in self.read_from_file():
            tmp = line.split()
            board.append((tmp[0], int(tmp[1])))
        board.append((name, score))
        board.sort(key=lambda tup: tup[1], reverse=True)
        with open(self.file_path, "w") as file:
            for i in range(min(len(board), settings.LEADERBOARD_LENGTH)):
                file.write("{} {}\n".format(board[i][0], str(board[i][1])))
