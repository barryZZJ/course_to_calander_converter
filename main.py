import argparse
import os
from courseadder import *
import regex

parser = argparse.ArgumentParser()

parser.add_argument("-j","--json", default="new/template.json", help="path to json file, default is new/template.json")
parser.add_argument("first", help="first day of semester, yyyy-mm-dd")
parser.add_argument("-n", "--name", default="课表", help="set output filename, default is 课表")

def assertWarning(boolv, msg):
    if not boolv:
        print(msg)
        exit(-1)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.json
    assertWarning(os.path.exists(path), f"json file {path} does not exists!")
    assertWarning(os.path.splitext(path)[1].endswith("json"), f"{path} is not json file")
    contents = normalize_file_json(path)
    firstdaystr = args.first
    match = regex.match("(\d{4})-(1[0-2]|0?[1-9])-([12][0-9]|3[01]|0?[1-9])", firstdaystr)
    try:
        firstday = datetime(*map(int, match.groups()))
    except Exception as e:
        assertWarning(False, e)

    courses = make_courses(contents, firstday)
    mycal = MyCalendar()
    for i, course in enumerate(courses):
        print("Processing Course {}...".format(i))
        add_course(mycal, course)
    mycal.save_as_ics_file(args.name)
    print("Done!")