import turtle

# 함수 선언 부분

    
# 변수 선언 부분
myT = None

#메인 코드 부분
    
myT = turtle.Turtle()
myT.shape('turtle')

for i in range(0, 120) :
    myT.speed(200)
    myT.forward(i)
    myT.right(30)
    myT.color('blue')

for i in range(0, 120) :
    myT.speed(200)
    myT.forward(i)
    myT.right(30)
    myT.color('red')

for i in range(0, 120) :
    myT.speed(200)
    myT.forward(i)
    myT.right(30)
    myT.color('green')    

myT.done()
