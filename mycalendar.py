import datetime
import os
import uuid

# ics文件里时间顺序不影响
class Event:
    """
    事件对象
    """

    def __init__(self, kwargs):
        self.event_data = kwargs

    def to_string(self):
        event_texts = []
        event_texts.append("BEGIN:VEVENT")
        for item, data in self.event_data.items():
            item = str(item).replace("_", "-")
            if item not in ["DTSTART", "DTEND"]:
                event_texts.append(f"{item}:{data}")
            else:
                event_texts.append(f"{item};{data}")
        event_texts.append("END:VEVENT")
        return "\n".join(event_texts)


class MyCalendar:
    """
    日历对象
    """

    def __init__(self):
        self.__events__ = {}
        self.__event_id__ = 0
        self.__calendar_header = """BEGIN:VCALENDAR
            PRODID:iCal Import/Export CalDAV 3.1
            VERSION:2.0
            BEGIN:VTIMEZONE
            TZID:Asia/Shanghai
            TZURL:http://tzurl.org/zoneinfo/Asia/Shanghai
            X-LIC-LOCATION:Asia/Shanghai
            BEGIN:STANDARD
            TZOFFSETFROM:+080543
            TZOFFSETTO:+0800
            TZNAME:CST
            DTSTART:19010101T000000
            RDATE:19010101T000000
            END:STANDARD
            BEGIN:DAYLIGHT
            TZOFFSETFROM:+0800
            TZOFFSETTO:+0900
            TZNAME:CDT
            DTSTART:19400602T230000
            RDATE:19400602T230000
            RDATE:19410315T230000
            RDATE:19860504T000000
            RDATE:19870412T000000
            RDATE:19880410T000000
            RDATE:19890416T000000
            RDATE:19900415T000000
            RDATE:19910414T000000
            END:DAYLIGHT
            BEGIN:STANDARD
            TZOFFSETFROM:+0900
            TZOFFSETTO:+0800
            TZNAME:CST
            DTSTART:19400930T230000
            RDATE:19400930T230000
            RDATE:19410930T230000
            RDATE:19860913T230000
            RDATE:19870912T230000
            RDATE:19880910T230000
            RDATE:19890916T230000
            RDATE:19900915T230000
            RDATE:19910914T230000
            END:STANDARD
            BEGIN:STANDARD
            TZOFFSETFROM:+0800
            TZOFFSETTO:+0800
            TZNAME:CST
            DTSTART:19490101T000000
            RDATE:19490101T000000
            END:STANDARD
            END:VTIMEZONE""".replace(" ", "") # 日历头，replace 用来去掉对齐用的缩进

    def add_event(self, **kwargs):
        event = Event(kwargs)
        event_id = self.__event_id__
        self.__events__[self.__event_id__] = event
        self.__event_id__ += 1
        return event_id

    def modify_event(self, event_id, **kwargs):
        for item, data in kwargs.items():
            self.__events__[event_id].event_data[item] = data

    def remove_event(self, event_id):
        self.__events__.pop(event_id)

    def get_ics_text(self):
        texts = [self.__calendar_header]
        for value in self.__events__.values():
            texts.append(value.to_string())
        texts.append("END:VCALENDAR")
        self.__calendar_text__ = "\n".join(texts)
        return self.__calendar_text__

    def save_as_ics_file(self, filename):
        ics_text = self.get_ics_text()
        with open(f"output/{filename}.ics", "w", encoding="utf8") as f:
            f.write(ics_text)

