    ## 계산기 ##
a = int(input("첫 번째 숫자를 입력하세요 : "))
b = int(input('두 번째 숫자를 입력하세요 : '))
c = int(input('세 번째 숫자를 입력하세요 : '))

result = a + b
print("덧셈 : ", a, '+', b, '=', result)

result = a - b
print("뺏셈 : ", a, '-', b, '=', result)

result = a * b
print("곱셈 : ", a, '*', b, '=', result)

result = a / b
print("나누기 : ", a, '/', b, '=', result)
result = a + b * c
print("덧셈과 곱셈 : ", a, '+', b, '*', c, '=', result, "\n")
    ## 줄 건너뛰기 ##
print("Hello \nWorld")

    ## 요일, 월, 일, 시, 분, 초, 년도 ##
from datetime import datetime
now = datetime.now().strftime('%c')
print("현재 시간 : ", now)
