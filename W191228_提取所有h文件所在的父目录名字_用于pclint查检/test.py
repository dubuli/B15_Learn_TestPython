import sys, os
listtmp = ["D:\sdf\sf\sfdasdfas.h", "D:\sdf\sf\sfdasdfssdfas.h", "D:\sdf\sxxf\sdfasdfii.h", "D:\sdf\sf"]

listtmp2 = []
for strline in listtmp:
    strlinetmp = os.path.dirname(strline)
    if (".h" in strline) | (".H" in strline):
        strlinetmp = strline
        # i  = strlinetmp.str
        strlinetmp = ("-i\"" + os.path.dirname(strline) + "\\\"")
        if strlinetmp not in listtmp2:
            listtmp2.append(strlinetmp) 

str_all = "\n".join(listtmp2)

f = open("txt.txt", "w+")
f.write(str_all)
f.close()


pass