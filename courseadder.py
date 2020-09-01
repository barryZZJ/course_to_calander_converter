from datetime import datetime, date, time, timedelta
from mycalendar import Event, MyCalendar
from converter import read_file, normalize_file, make_courses
from course import Course
import uuid

# 把课程加入日历中
def add_course(cal: MyCalendar, course: Course):
    for loc, times in course.course_times.items():
        descrip = "任课教师:{}".format(course.instr_name)
        # times: [(上课时间, 下课时间), ...]
        for st, ed in times:
            add_event(cal, st, ed, "Phone", course.course_name, descrip, loc)


def add_event(cal: MyCalendar, DTSTART: datetime, DTEND: datetime, ORGANIZER, SUMMARY, DESCRIPTION, LOCATION):
    """
    向Calendar日历对象添加事件的方法
    :param cal: calender日历实例
    :param SUMMARY: 事件名
    :param DTSTART: 事件开始时间
    :param DTEND: 时间结束时间
    :param DESCRIPTION: 备注
    :param LOCATION: 时间地点
    :return:
    """
    time_format = "TZID=Asia/Shanghai:{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}{date.second:0>2d}"
    dt_start = time_format.format(date=DTSTART)
    dt_end = time_format.format(date=DTEND)
    create_time = datetime.today().strftime("%Y%m%dT%H%M%SZ")
    cal.add_event(
        DTSTART=dt_start,
        TRANSP="OPAQUE",
        DTEND=dt_end,
        ORGANIZER=ORGANIZER,
        SUMMARY=SUMMARY,
        DESCRIPTION=DESCRIPTION,
        LOCATION=LOCATION,
        STATUS="CONFIRMED",
        DTSTAMP=create_time,
        UID="{}".format(uuid.uuid4())
    )

if __name__ == "__main__":
    contents = normalize_file(
        r"D:\Software\Pycharm\Projects\生成课表\courseinfo.csv")
    courses = make_courses(contents, datetime(2020, 8, 31))
    mycal = MyCalendar()
    for i, course in enumerate(courses):
        print("Processing Course {}...".format(i))
        add_course(mycal, course)
    mycal.save_as_ics_file("大三上课表")
    print("Done!")