import numpy as np
from time import time
import csv
from glob import glob
from os import remove
from KeyRecord import KeyRecord
import Login
from keyboard import record as recording

class DataManager:
    def __init__(self, _datapath, _tagname):
        self.datapath = _datapath
        self.tagname = _tagname

    def loadData(self):

        patterns = glob(self.datapath + '*.csv')
        X = np.zeros((len(patterns), 13))   # tmp value : 13
        # self.n_current = len(patterns)
        # self.n_valid = int(self.n_current * 0.3)
        # X = np.zeros((self.n_current, self.n_pattern))

        for i in range(len(patterns)):
            x = []

            with open(patterns[i], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x.append(row['times'])
            X[i] = x
        # X = X[:,:2]
        return X

    def upDate(self, times):
        file_name = str(int(time()))
        with open(self.datapath + file_name + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['times']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(len(times)):
                writer.writerow({'times': times[i]})

        # if self.n_patterns is self.n_current:
        #     patterns = glob(self.file_path + '*.csv')
        #     patterns.sort()
        #     if self.debug:
        #         print('[debug] remove ', patterns[0])
        #     remove(patterns[0])

    def getFilepath(self):
        return self.datapath

    def setFilepath(self, _datapath):
        self.datapath = _datapath

    def getTagname(self):
        return self.tagname

    def setTagname(self, _tagname):
        self.tagname = _tagname


    def _preprocess(self, x):
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

    res = user1.loadData()

    print(res)

