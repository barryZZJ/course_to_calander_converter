from typing import List, Tuple, Optional, Union, Any, Dict
from datetime import datetime, date, time, timedelta
from timetable import TimeTable
from course import Course
import numpy 
import regex
import json

char2int = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "日": 7,
    "天": 7
}

def make_course_times(course_name, texts: List[List], first_day_of_semester: datetime, time_table=TimeTable()):
    """
    texts格式：
        [ ["a,b,c...":周数, D[e-f节], 教室号], [...] ]
        e.g.: 
        [['1,2,3', '四[3-4节]', 'D1151']
         ['11,12,13', '六[3-4节]', 'D1138']]
    
    return: Dict{ 教室号: [(上课时间, 下课时间), ...] }
    """
    course_time = {}
    for text in texts:
        # weeks 数组, 第几周 : int
        weeks = map(int, text[0].split(","))
        
        reg_res = regex.findall(r"(.)\[(\d+)-(\d+)节\]", text[1])[0]
        if len(reg_res) == 0:
            raise(BaseException("正则表达式查找出错！\n{}".format(text[1])))
        day, st, ed = reg_res
        # day: 星期几 : int
        day = char2int[day]
        # st, ed: 上课，下课时间 : time
        try:
            st = time_table[int(st)][0]
            ed = time_table[int(ed)][1]
        except KeyError as err:
            raise(KeyError(f"{course_name} 课程节次输入错误，请检查！"))
        
        # loc: 教室        
        loc = text[2]
        
        course_time.setdefault(loc, list())
        
        for week in weeks:
            st_offset = timedelta(weeks=week-1, days=day-1, hours=st.hour, minutes=st.minute, seconds=st.second)
            ed_offset = timedelta(weeks=week-1, days=day-1, hours=ed.hour, minutes=ed.minute, seconds=ed.second)
        
            course_time[loc].append(
                (first_day_of_semester + st_offset,
                 first_day_of_semester + ed_offset)
            )
            # print(f"{loc}: {course_time[loc][-1]}")
    return course_time

def make_courses(contents, first_day_of_semester: datetime):
    courses = []
    for content in contents:
        course_name, instructor_name, *course_time_texts = content
        if (len(course_time_texts) % 3 != 0):
            raise(BaseException(f"{course_name} 课程时间输入错误，请检查！"))
        course_time_texts = numpy.reshape(course_time_texts, (-1, 3))
        course_times = make_course_times(course_name, course_time_texts, first_day_of_semester)
        
        course = Course(course_name, instructor_name, course_times)
        # print(course_name, instructor_name)
        courses.append(course)
    return courses
        
#! 还不知道一周多节相同教室时text的格式如何，最好还是一个教室对应每周的一次课
def read_file(filepath):
    """
    读入csv文件，用空格为分隔符，每一行读入为一个数组
    
    return: e.g. 
    [['操作系统', '何静媛', '1-7,8-14', '四[3-4节]', 'D1151', '1-13', '六[3-4节]', 'D1138'], 
    ['世界舞台上的中华文明', '叶泽川', '15,16', '四[10-11节]', '4,7,9,11,13', '10,11', 'D1545']]
    """
    contents = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                contents.append(line.strip().split(" "))

    return contents

def normalize_file(filepath, read_only=False):
    """
    把周次 a-b周 详存回csv文件里
    细写出，并
    return: e.g. 
    [['操作系统', '何静媛', '1,2,3,4,7,8,9,10,11,12,13,14', '四[3-4节]', 'D1151', '1,2,3,4,6,7,8,9,10,11,12,13', '六[3-4节]', 'D1138'], 
    ['世界舞台上的中华文明', '叶泽川', '15,16', '四[10-11节]', '4,7,9,11,13', '10,11', 'D1545']]
    """
    contents = read_file(filepath)
    if read_only:
        return contents
    
    for content in contents:
        for i in range(2, len(content), 3):
            if "-" in content[i]:
                wks = list()
                l = content[i].split(",")
                for s in l:
                    if "-" not in s:
                        wks.append(s)
                    else:
                        a, b = regex.findall(r"(\d+)-(\d+)", s)[0]
                        a, b = int(a), int(b)
                        wks.extend(map(str, range(a, b+1)))
                content[i] = ",".join(wks)
                
    with open(filepath, "w", encoding="utf-8") as f:
        for content in contents:
            f.write(" ".join(content))
            f.write("\n")
    return contents

def read_file_json(filepath):
    """
        读入json文件，用空格为分隔符，每一行读入为一个数组

        return: e.g.
        [['操作系统', '何静媛', '1-7,8-14', '四[3-4节]', 'D1151'],
         ['操作系统', '何静媛', '1-13', '六[3-4节]', 'D1138'],
         ['世界舞台上的中华文明', '叶泽川', '15,16', '四[10-11节]'],
         ['世界舞台上的中华文明', '叶泽川', '4,7,9,11,13', '四[10-11节]', 'D1545']]
        """
    contents = []
    with open(filepath, 'r', encoding='utf8') as f:
        datas = json.load(f)
    for data in datas["data"]:
        course = [data['courseName'], data['classTimetableInstrVOList'][0]['instructorName'], data['teachingWeekFormat'], f"{data['weekDayFormat']}[{data['periodFormat']}节]", data['roomName']]
        if 'None' in course[3]:
            # 跳过节数含有None的课
            continue
        contents.append(course)

    return contents

def normalize_file_json(filepath, read_only=False):
    """
        把周次 a-b周 展开
        return: e.g.
        [['操作系统', '何静媛', '1,2,3,4,7,8,9,10,11,12,13,14', '四[3-4节]', 'D1151', '1,2,3,4,6,7,8,9,10,11,12,13', '六[3-4节]', 'D1138'],
        ['世界舞台上的中华文明', '叶泽川', '15,16', '四[10-11节]', '4,7,9,11,13', '10,11', 'D1545']]
        """
    contents = read_file_json(filepath)
    if read_only:
        return contents

    for content in contents:
        for i in range(2, len(content), 3):
            if "-" in content[i]:
                wks = list()
                l = content[i].split(",")
                for s in l:
                    if "-" not in s:
                        wks.append(s)
                    else:
                        a, b = regex.findall(r"(\d+)-(\d+)", s)[0]
                        a, b = int(a), int(b)
                        wks.extend(map(str, range(a, b + 1)))
                content[i] = ",".join(wks)

    # with open(filepath, "w", encoding="utf-8") as f:
    #     for content in contents:
    #         f.write(" ".join(content))
    #         f.write("\n")
    return contents
