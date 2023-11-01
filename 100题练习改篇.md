#三位数各位不同数字
# for i in range(1,5):
#     for j in range(1,5):
#         for k in range(1,5):
#             if( i != k ) and (i != j) and (j != k):
#                 print (i,j,k)
#高级写法列表推导式
# result = [(i, j, k) for i in range(1, 5) for j in range(1, 5) for k in range(1, 5) if (i != k) and (i != j) and (j != k)]
# print(result)
#生成器和迭代器写法
result = ((i, j, k) for i in range(1, 5) for j in range(1, 5) for k in range(1, 5) if (i != k) and (i != j) and (j != k))
#利用该可迭代对象的可迭代性质
# for x in result:
#     print(x)
#对象转换调用
d=iter(result)
while 1:
    try:
        tuple=next(d)
        three_digit_number = int(''.join(map(str, tuple)))
        print(three_digit_number)
    except StopIteration:
        break
# 坐标索引法依据纯利润计算利润总和
# i=int(input('净利润'))
# arr=[1000000,600000,400000,200000,100000,0]
# rat = [0.01,0.015,0.03,0.05,0.075,0.1]
# r=0
# for idx in range(0,6):
#     if i>arr[idx]:
#         r+=(i-arr[idx])*(rat[idx])
#         print((i-arr[idx])*(rat[idx]))
#         i=arr[idx]
#         print(i)
# print(r)
#题目：一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？
#1、x  = n2-100, x = m2-(100 + 168)
# for j in range(1,85):
#     if 168%j==0:
#         i=168/j
#         if j>i and (j+i)%2==0 and (j-i)%2==0:
#             m = (j + i) / 2
#             n = (j - i) / 2
#             x=n*n-100
#             y=m*m-268
#             print(x)
#             print(y)
# 交换i j位置同样算法成立，等价式子也可替换
#题目：输入某年某月某日，判断这一天是这一年的第几天？
#程序分析：以3月5日为例，应该先把前两个月的加起来，然后再加上5天即本年的第几天，特殊情况，闰年且输入月份大于2时需考虑多加一天：
# !/usr/bin/python3
year = int(input('year:\n'))
month = int(input('month:\n'))
day = int(input('day:\n'))
months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
if 0 < month <= 12:
    sum = months[month - 1]
else:
    print('data error')
sum += day
leap=0
# if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
#     leap = 1
# if (leap == 1) and (month > 2):
#     sum += 1
    #反转条件
# if not((year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0))):

   #不必反转正写
# if (year % 400 != 0) and ((year % 4 != 0) or (year % 100 == 0)):
#     leap = 0
# if (leap == 1) and (month > 2):
#     sum += 1
# print('it is the %dth day.' % sum)
