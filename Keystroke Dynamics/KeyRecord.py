from keyboard import record as recording
from time import sleep


class KeyRecord:
    def __init__(self):
        self.names = None
        self.times = None

    def record(self, records):
        names = []
        times = []

        if records[0].name == 'enter' and records[0].event_type == 'up':
            records = records[1:]

        t0 = records[0].time
        # cause leaf element is enter, not check.
        for i in range(len(records) - 1):
            if records[i].event_type == 'down':
                if records[i].name == 'space':
                    records[i].name = ' '
                if records[i].name == 'shift':
                    if i != 0 and records[i - 1].name == 'shift':
                        times = times[:-1]
                        continue
                    else:
                        records[i].name = ''

                if records[i].name == 'backspace':
                    times = times[:-1]
                    names = names[:-1]

                if records[i].name == 'delete':
                    times = times[:-1]
                    names = names[:-1]

                else:
                    times.append(records[i].time - t0)
                    names.append(records[i].name)

        name = ''.join(names)

        self.times = times
        self.names = name

        return times, name

    def getNames(self):
        return self.names

    def getTimes(self):
        return self.times

    def getTotaltimes(self):
        return self.times[-1] - self.times[0]


# for module testing.
if __name__ == "__main__":
    kr = KeyRecord()
    print("Test Line input")
    print("[ID] : ")
    T, N = kr.record(recording(until='enter'))
    sleep(0.5)

    print(T)
    print(N)

    print("[PW] : ")
    PW_data = recording(until='enter')
    sleep(0.5)
    T, N = kr.record(PW_data)

    print(T)
    print(N)

    print(kr.names is N)
    print(kr.times is T)
    print(kr.getTotaltimes() is (T[-1] - T[0]))
