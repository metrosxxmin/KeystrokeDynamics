import numpy as np
from time import time
import csv
from glob import glob
from keyboard import record as recording
from KeyRecord import KeyRecord
from os import remove


class DataManager:
    def __init__(self, _datapath, _tagname):
        self.datapath = _datapath
        self.tagname = _tagname

    def loadData(self):
        patterns = glob(self.datapath + '*.csv')
        X = []

        for i in range(len(patterns)):
            x = []

            with open(patterns[i], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x.append(row['times'])
            X.append(x)
        return np.array(X)

    def upDate(self, times):
        file_name = str(int(time()))
        with open(self.datapath + file_name + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['times']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(len(times)):
                writer.writerow({'times': times[i]})

        if len(glob(self.datapath + '*.csv')) > 20:
            patterns = glob(self.datapath + '*.csv')
            patterns.sort()
            remove(patterns[0])

    def getFilepath(self):
        return self.datapath

    def setFilepath(self, _datapath):
        self.datapath = _datapath

    def getTagname(self):
        return self.tagname

    def setTagname(self, _tagname):
        self.tagname = _tagname

    def preprocess(self, x):
        if len(x.shape) == 1:
            x_copy = np.zeros(len(x) - 1)
            for i in range(len(x) - 1, 0, -1):
                x_copy[i - 1] = x[i] - x[i - 1]
                x_copy[i - 1] = np.log(x_copy[i - 1])

        if len(x.shape) == 2:
            x_copy = np.zeros((x.shape[0], x.shape[1] - 1))
            for i in range(len(x)):
                for j in range(len(x[i]) - 1, 0, -1):
                    x_copy[i][j - 1] = x[i][j] - x[i][j - 1]
                    x_copy[i][j - 1] = np.log(x_copy[i][j - 1])

        return x_copy


# for module testing & creating initial data set.
if __name__ == "__main__":
    PATH_STORE_SOOMIN = "/Users/sxxmin/github/Keystroke/Keystroke Dynamics/soomin/"
    user1 = DataManager(PATH_STORE_SOOMIN, "soomin.txt")

    kr = KeyRecord()
    kr2= KeyRecord()
    for i in range(0, 20):
        kr.record(recording(until='enter'))
        kr2.record(recording(until='enter'))
        X = user1.preprocess(np.array(kr.times))
        X = np.hstack([X, user1.preprocess(np.array(kr2.times))])
        X = np.hstack([X, kr.times])
        X = np.hstack([X, kr2.times])
        X = np.hstack([X, kr.getTotaltimes()])
        X = np.hstack([X, kr2.getTotaltimes()])
        user1.upDate(X)
