myList=[30,10,20]
print("현재 리스트 : %s" % myList)
###맨 뒤에 40 추가
myList.append(40)
print("append(40) 후의 리스트 : %s" % myList)
###맨 뒤에 40 추출
print("pop()으로 추출한 값 : %s" % myList.pop())
print("pop() 후의 리스트 : %s" % myList)
###오름차순 정렬
myList.sort()
print("sort() 후의 리스트 : %s" % myList)
###역순 정렬
myList.reverse()
print("reverse() 후의 리스트 : %s" % myList)
###해당 위치 순서
print("20값의 위치 %d" % myList.index(20))
###지정된 위치에 222 추가
myList.insert(2, 222)
print("myList.insert(2, 222) 후의 리스트 : %s" % myList)
###지정한 값 삭제
myList.remove(222)
print("remove(222) 후의 리스트 : %s" % myList)
###추가 할 리스트
myList.extend([77, 88, 77])
print("extend([77, 88, 77]) 후의 리스트 : %s" % myList)
### 찾을 값 개
print("77값의 개수 : %d" % myList.count(77))
