print("%d" % 123)
print("%5d" % 123)
print("%05d\n" % 123)

print("%f" % 123.45)
print("%7.1f" % 123.45)
print("%7.3f\n" % 123.45)

print("%s" % "Python")
print("%10s\n" % "Python")

print("%d %5d %05d" % (123, 123, 123))
print("{0:d} {1:5} {2:05d}\n".format(123, 123,123))

print("{0:s} {1:5} {2:05d}\n".format("123", 123,123))
print("\n")

print("한 행입니다. 또 한 행입니다.")
print("한 행입니다. \n또 한 행입니다.")
print("한 행입니다. \t한 행입니다.")
print("한 행입니다. \b한 행안 행.")
print("한 행입니다. " "\r\b한 행 안 행.")
print("\n")

s= "안녕\r하세요"
print(s)


print("\n줄바꿈\n연습")
print("\t탭키\t연습")
print("글자가 \"강조\"되는 효과1")
print("글자가 \'강조\'되는 효과2")
print("\\\\\\ 역슬래시 세 개 출력")
print(r"\n \t \" \\를 그대로 출력")
