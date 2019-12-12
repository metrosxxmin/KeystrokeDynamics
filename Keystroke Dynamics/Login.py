import numpy as np
from keyboard import record as recording
from DataManager import DataManager
from KeyRecord import KeyRecord
from glob import glob
from time import time
from os import remove, system
import sys
import csv
from KeyGraph import KeyGraph
from sklearn import mixture
#from DataManager import DataManager


class Login:
    def __init__(self, _n_patterns, _threshold, _update):
        self.n_current = None
        self.n_pattern = None
        self.n_patterns = _n_patterns
        self.n_valid = None
        self.threshold = _threshold
        self.update = _update

    def _getDifference(self, X, y, weights=None):
        if weights is None:
            weights = np.ones(len(y))

        cand_score = []
        for i in range(len(X)):
            diff = np.abs(np.array(X[i], dtype=float) - np.array(y, dtype=float))
            cand_score.append(np.dot(diff, weights))
        return np.min(cand_score), np.argmin(cand_score)

    def typingCheck(self):
        while True:
            print("[id]: ")
            info_id.record(recording(until='enter'))

            print("\n[pw]: ")
            info_pw.record(recording(until='enter'))

            f = open(userID.datapath + userID.tagname)
            ID_line = f.readline()
            ID_line = ID_line.replace("\n", "")
            PW_line = f.readline()
            PW_line = PW_line.replace("\n", "")

            if (ID_line == info_id.names) and (PW_line == info_pw.names):
                break
            else:
                print("\nYour ID or password is wrong. Please retry.")

        f.close()

        id_time_data = userID.preprocess(np.array(info_id.times))
        pw_time_data = userID.preprocess(np.array(info_pw.times))
        time_data = np.append(id_time_data, pw_time_data, axis=0)

        time_data2= np.append(info_id.times, info_pw.times)

        id_total_T = info_id.getTotaltimes()
        pw_total_T = info_pw.getTotaltimes()

        target = np.append(time_data, time_data2, axis=0)
        target = np.hstack([target, id_total_T])
        target = np.hstack([target, pw_total_T])

        self.n_pattern = len(target)
        X = userID.loadData()

        if self.recognition(X, target):
            print("\nsuccess")
            userID.upDate(target)
            return True
        else:
            print("\nfail")
            return False

    def recognition(self, Xp, yp):
        yp = yp.astype(Xp.dtype)

        if self.getNcurrent() < int(self.getNpatterns() * 0.5):
            print("data가 충분치 않습니다")
            return True

        score = 0
        weights = self.getWeight(Xp)
        # weights = np.ones(yp.shape)/len(yp)

        for i in range(self.getNcurrent() - self.getNvalid(), self.getNcurrent()):
            med_score, _ = self._getDifference(Xp[:-self.getNvalid()], Xp[i], weights=weights)

            score += med_score / self.getNvalid()

        input_score, _ = self._getDifference(Xp[:-self.getNvalid()], yp, weights=weights)

        if input_score <= score * self.getThreshold():
            return True

        return False

    def getWeight(self, X):
        X = np.array(X)
        weights = np.ones(np.array(X[0]).shape) / len(X[0]) * 100

        kg = KeyGraph()
        f = open(userID.datapath + userID.tagname)
        line = f.readline()
        line = line.replace("\n", "")
        f.close()
        for i in range(len(line) - 1):
            if kg.isChain(line[i], line[i + 1]):
                weights[i] = 0

        return weights

    def getNpatterns(self):
        return self.n_patterns

    def getNpattern(self):
        return self.n_pattern

    def getNcurrent(self):
        return len(glob(PATH_STORE_SOOMIN + '*.csv'))

    def getNvalid(self):
        return int(self.getNcurrent() * 0.3)

    def getThreshold(self):
        return self.threshold

    def setThreshold(self, _threshold):
        self.threshold = _threshold





# def validation(train_path, test_paths, debug=True, threshold=1.5):
#     k1 = Login(train_path, threshold=threshold, debug=False, n_patterns=20, update=False)
#
#     score = 0
#     total = 0
#
#     score1 = 0
#     total1 = 0
#
#     score2 = 0
#     total2 = 0
#
#     test_paths = glob(test_paths + "**/")
#     for test_path in test_paths:
#         f = open(test_path + "answer.txt", 'r')
#         label = bool(f.readline().replace('\n', ''))
#
#         f.close()
#
#         csv_paths = glob(test_path + "*.csv")
#
#         for csv_path in csv_paths:
#
#             y = []
#             with open(csv_path, newline='') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 for row in reader:
#                     y.append(row['times'])
#
#             xlabel = k1.login(y)
#             if label:
#                 if xlabel:
#                     score += 1
#                     score1 += 1
#                 total1 += 1
#             else:
#                 if xlabel:
#                     score2 += 1
#                 else:
#                     score += 1
#                 total2 += 1
#             total += 1
#             if debug:
#                 print("ans:", label, "guess:", xlabel)
#                 print(score, total)
#                 print()
#     return score / total, score1 / total1, score2 / total2




if __name__ == '__main__':
    PATH_STORE_SOOMIN = "/Users/sxxmin/github/Keystroke/Keystroke Dynamics/soomin/"
    userID = DataManager(PATH_STORE_SOOMIN, "soomin.txt")
    info_id = KeyRecord()
    info_pw = KeyRecord()
    login = Login(20, 1.5, True)

    login.typingCheck()


    # train = "/Users/sxxmin/PycharmProjects/KeystrokeDynamics/train/"
    # test = "/Users/sxxmin/PycharmProjects/KeystrokeDynamics/test2/"
    #
    # ret, ret1, ret2 = validation(train, test, threshold=1.0, debug=False)
    # print("성공률:", ret)
    #
    # min_thres = 1.40
    # max_thres = 1.80
    # n = 40
    # for i in range(n):
    #     threshold = min_thres + (max_thres - min_thres) * i / n
    #     ret, ret1, ret2 = validation(train, test, threshold=threshold, debug=False)
    #     print("성공률:", ret, threshold)
    # # print("jh 성공률:",ret1)
    # # print("yt 성공률:",ret2)
    #
    # '''
    # k1 = KeyStroke('./test/yt/',debug = True,n_patterns = 40,update = True)
    # while True:
    #     k1.login()
    #     sys.stdout.flush()
    # '''

