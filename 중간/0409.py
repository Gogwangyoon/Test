'''print("10진수 ", bin(11), bin(0o11), bin(0x11)) # 10진수

print(oct(11), oct(0b11), oct(0x11)) # 8진수

print(hex(11), hex(0b11), hex(0o11)) # 16진수'''

sel = int(input("입력 진수 결정(16/10/8/2) : ")) 
num = input("값 입력 : ")

if sel == 16 :
    num10 = int(num, 16)
if sel == 10 :
    num10 = int(num, 10)
if sel == 8 :
    num10 = int(num, 8)
if sel == 2 :
    num10 = int(num, 2)

print("\n16진수 ==> ", hex(num10))
print("10진수 ==> ", num10)
print("8진수 ==> ", oct(num10))
print("2진수 ==> ", bin(num10))
