# course_to_calander_converter
根据课程表生成日历文件.ics，用于导入手机日历。

适用于新版选课网 my.cqu.edu.cn/enroll/



## 使用说明

1. 获取课表信息json文件。

   在[选课管理页面](my.cqu.edu.cn/enroll/Home)点击查看课表，用抓包工具获得选课信息的json文件，命名为`template.json`放入`new/`中。

2. 生成ics日历文件，修改courseadder.py中的入口main函数：

   1. line47，修改调用make_courses的第二个参数为本学期第一天

   3. 可选：line52，修改生成ics的默认文件名

3. 导入到手机日历。

   方法一：（安卓，ios通用）
   1. 把ics文件用邮件的方式发给自己，然后用手机或ipad打开，即可导入。
   
   
   方法二：（仅限安卓）
   1. 安装用于导入ics文件的app：[iCal Import/Export.apk](https://github.com/barryZZJ/course_to_calander_converter/raw/master/iCal%20Import%20Export.apk)（已经上传到repo里了，链接点不开的话就把整个库下载下来）
   1. （可选）可以先点 EDIT CALENDARS 新建一个专门存课表的日历
   2. 选IMPORT，进去后Import source选Internal/External memory，文件路径就是刚刚生成的ics文件，然后一路下一步就行了

   

P.S. 上课下课时间可以在 timetable.py 里进行相应的修改

P.P.S 日历头(MyCalendar.__calendar_header) 那一堆东西可以导出自己手机的日历参照着改一下，我用的是我手机导出来的，在别的日历上应该没啥大问题，懒得改的话也可以不管。



## 废话

第一版：我用着没啥大问题，如果有bug建议自己改改代码。不过有问题、意见建议啥的还是可以在Issues里提的哈。

第二版：适配了新版选课网，可以直接获取json文件处理起来更方便了。

TODO 把抓包那个过程变成自动化的登录统一认证平台
TODO 把要修改的代码变成参数传入

没啥大用的小程序我就不求star了~



## 参考资料

[使用python生成ical日历文件——将课程表导入到手机日历](https://www.cnblogs.com/zhongbr/p/python_calender.html)