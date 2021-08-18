
import os
filePath = 'C:\\Users\\wyc\\Downloads\\th14东方辉针城汉化版+1.00b日文版'
list=os.listdir(filePath)
for i in list:
    if i[-3:]=="anm":
        print("thanm.exe -x "+i)
