from datetime import time

# 每节课的时间
class TimeTable:
    def __init__(self):
        self._data = {
            1: [time(8, 30), time(9, 15)],
            2: [time(9, 25), time(10, 10)],
            3: [time(10, 30), time(11, 15)],
            4: [time(11, 25), time(12, 10)],
            5: [time(13, 30), time(14, 15)],
            6: [time(14, 25), time(15, 10)],
            7: [time(15, 20), time(16, 5)],
            8: [time(16, 25), time(17, 10)], 
            9: [time(17, 20), time(18, 5)],
            10: [time(19, 0), time(19, 45)],
            11: [time(19, 55), time(20, 40)],
            12: [time(20, 50), time(21, 35)],
            13: [time(21, 45), time(22, 30)]
        }
    
    def __getitem__(self, key):
        return self._data[key]

if __name__ == "__main__":
    tb = TimeTable()
    print(tb[1][0])