"""Handle game statistics."""

import pickle
import os


class Stat:
    """Statistics class."""

    def __init__(self):
        """Create new statistic."""
        self.__data = {
            'gametime': 0,
            'win': 0,
        }
        self.__old = []
        self.__file = None

    def __getitem__(self, attr):
        """Access statistic."""
        if attr in self.__data:
            return self.__data[attr]
        raise ValueError(f'Unknown item {attr} to access statistic')

    def __setitem__(self, attr, val):
        """Set statistic."""
        if attr in self.__data:
            self.__data[attr] = val
        else:
            raise ValueError(f'Unknown item {attr} to access statistic')

    def assignFile(self, name):
        """Assign some file to statistic."""
        self.filepath = os.getcwd() + os.sep + "stat" + os.sep + name + ".bin"
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'wb') as f:
                pickle.dump([], f)
        return self.filepath

    def readStatistic(self):
        """Read old statistic."""
        with open(self.filepath, 'rb') as f:
            self.__old = pickle.load(f)

    def saveStatistic(self):
        """Save current statistic."""
        with open(self.filepath, 'wb') as f:
            pickle.dump([*self.__old, list(self.__data.values())], f)

    def findBest(self):
        """Return best statistic values at all time."""
        bestWinTime = self['gametime'] if self['win'] else 0
        meanWinTime = self['gametime'] if self['win'] else 0
        gamesWon = int(self['win'])
        for history in self.__old:
            hTime, hWin = history
            gamesWon += hWin
            if hWin:
                meanWinTime += hTime
                if bestWinTime > hTime:
                    bestWinTime = hTime
        meanWinTime = 0 if gamesWon == 0 else meanWinTime / gamesWon
        return bestWinTime, meanWinTime, gamesWon

    def print(self):
        """Print statistic and it's best."""
        bestWinTime, meanWinTime, gamesWon = self.findBest()
        winPercent = gamesWon / (len(self.__old) + 1) * 100
        print('Current game time:', self['gametime'], 'seconds')
        print('Best win time:    ', bestWinTime, 'seconds')
        print('Games played:     ', len(self.__old) + 1)
        print('Games won:        ', gamesWon)
        print(f'Win percent:       {winPercent:.2f}')
        print('Mean win time:    ', meanWinTime, 'seconds')
