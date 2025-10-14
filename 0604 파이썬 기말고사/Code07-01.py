'''aa = [0, 0, 0, 0]
hap = 0
aa[0] = int(input("1번째 숫자 : "))
aa[1] = int(input("2번째 숫자 : "))
aa[2] = int(input("3번째 숫자 : "))
aa[3] = int(input("4번째 숫자 : "))

hap = aa[0] + aa[1] + aa[2] + aa[3]

x = 8
print(f"정수형 객체 x의 식별자 (메모리 주소): {id(x)}")'''
###
'''aa = []
for i in range(0, 100):
    aa.append(0)
len(aa)'''
###
'''aa=[]
for i in range(0, 4):
    aa.append(0)
hap = 0

for i in range(0, 4):
        aa[i] = int(input(str(i+1)+"번째 숫자 : "))
        hap = hap + aa[i]
    
print("합계 ==> %d" % hap)'''
###
aa=[]
bb=[]
value=0
for i in range(0,200):
    aa.append(i*2)
    value+=2
for i in range(0, 100):
    bb.append(aa[99-i])
print("bb[0]에는 %d이, bb[99]에는 %d이 입력됩니다." % (bb[0], bb[99]))
