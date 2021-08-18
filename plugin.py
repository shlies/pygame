a={}
i=0
while 1:
    a[i]=str(input())
    if a[i]=="1":
        break
    i+=1
for j in a:
    print("thanm.exe -x "+a[j])
