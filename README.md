# course_to_calander_converter
根据课程表生成日历文件.ics，用于导入手机日历。

默认课程表字符串格式来自于重庆大学。

（以前wecqu提供的一键导入日历的API接口好像挂了，我看手动导入也不麻烦，于是就手写了一个）



## 参考资料

[使用python生成ical日历文件——将课程表导入到手机日历](https://www.cnblogs.com/zhongbr/p/python_calender.html)

用于导入ics文件的app：[iCal Import/Export](./iCal Import Export.apk)



## 使用说明

1. 手写csv文件。

   参考courseinfo_template.csv 的格式（数据来自抢课网 “教学安排——查看个人课表”），注意分隔符是空格。

2. 生成ics文件（可直接参考courseadder.py中的main部分）。

   1. 调用 normalize_file(*filepath*)（converter.py ），其中filepath为csv文件的路径。得到返回值contents。

   2. 调用 make_courses(*contents*, first_day_of_semester: *datetime*)（converter.py ），得到返回值课程对象数组courses。

      （其中 first_day_of_semester 是本学期的第一天00:00对应的 datetime.datetime 对象）

   3. 生成 MyCalendar 对象 mycal（mycalendar.py) 
   4. 遍历courses，依次调用 add_course(cal: *MyCalendar*, course: *Course*)（courseadder.py），把每个课程的具体信息（课程名称，上课时间，下课时间等）添加到日历对象中。
   5. 调用 mycal 的 save_as_ics_file(*filename*) 成员函数，生成ics文件，发送到手机。（我生成的文件在output文件夹里，可以用来参考）

3. 导入到手机日历。

   1. （可选）可以先点 EDIT CALENDARS 新建一个专门存课表的日历
   2. 选IMPORT，进去后Import source选Internal/External memory，文件路径就是刚刚生成的ics文件，然后一路下一步就行了

   

P.S. 上课下课时间可以在 timetable.py 里进行相应的修改

P.P.S 日历头(MyCalendar.__calendar_header) 那一堆东西可以导出自己手机的日历参照着改一下，我用的是我手机导出来的，在别的日历上应该没啥大问题，懒得改的话也可以不管。



## 废话

第一版，我用着没啥大问题，如果有bug建议自己改改代码。不过有问题、意见建议啥的还是可以在Issues里提的哈。

没啥大用的小程序我就不求star了~