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
import time
# #斐波那契数列
# def faberi(n):
#     #这个条件可以n<=2
#     if n==1 or n==2:
#         return 1
#     else:
#         #可以改阶乘
#         return faberi(n-1)+faberi(n-2)
# start=time.time()
# print(faberi(40))
# end=time.time()
# print(f'{end-start}秒')

#动态规划
# def fibonacci(n):
#     fib = [0] * (n + 1)
#     print(f'创建了{len(fib)}个元素')
#     print(fib[0])
#     fib[1] = 1
#     for i in range(2, n + 1):
#         fib[i] = fib[i - 1] + fib[i - 2]
#     return fib[n]
# result = fibonacci(10)
#指定个数
# def fib(n):
#     if n == 1:
#         return [1]
#     if n == 2:
#         return [1, 1]
#     fibs = [1, 1]
#     for i in range(2, n):
#         fibs.append(fibs[-1] + fibs[-2])
#     return fibs
# 输出前 10 个斐波那契数列
# print(fib(3))
#简单for循环
# !/usr/bin/python
# -*- coding: UTF-8 -*-

# def fib(n):
#     a, b = 1, 1
#     for i in range(n - 1):
#         a, b = b, a + b
#     return a
# # 输出了第10个斐波那契数列
# print(fib(10))
#练习7
# 方法1将一个列表的数据复制到另一个列表中。
a = [1, 2, 3]
# b = a[:]
# print(b)
# 方法2将一个列表的数据复制到另一个列表中。
# b=[i for i in a]
# print(b)
# 方法3将一个列表的数据复制到另一个列表中,b为步长。
# b=a[::1]
# print(b)
# # 将一个列表的数据追加到另一个列表中。
#extend方法
list1 = [1,2,3]
list2=[]
list2.extend(list1)
print(list2)
#深拷贝和浅拷贝方法理解
>>> import copy
>>> a = [1,2,3,4,5]
>>> b = ["A","B",a]
>>> #浅拷贝
>>> c = b[:]
>>> c
['A', 'B', [1, 2, 3, 4, 5]]
>>> a[0] = 11
>>> c
['A', 'B', [11, 2, 3, 4, 5]]
>>> #此时a变化c跟着变化
>>> #深拷贝
>>> c = copy.deepcopy(b)
>>> c
['A', 'B', [11, 2, 3, 4, 5]]
>>> a[0] = 111
>>> a
[111, 2, 3, 4, 5]
>>> c
['A', 'B', [11, 2, 3, 4, 5]]
>>> #此时c中数据不受a影响
>>>
# c=[]
# for i in a:
#       c.append(i)
# print(c)
#九九乘法表
# for i in range(1,10):
#     print
#     for j in range(1,10):
#            print("%d*%d=%d"%(i,j,i*j),end=" ")
# !/usr/bin/python3

# for i in range(1, 10):
#     #控制运算的次数也是打印的行数
#     print(i)
#     for j in range(1, i + 1):
#         print("%d*%d=%d" % (i, j, i * j), end=" ")
#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ls = []
# for i in range(9):
#     s = []
#     for j in range(i+1):
#         s.append("{}*{}={}".format(i+1, j+1, (i+1)*(j+1)))
#     s = ' '.join(s)
#     ls.append(s)
#     if i != 8:
#         ls.append('\n')
# print(''.join(ls))
# for j in range(9):
#     i = 1
#     j = j + 1
#     while(i<=j):
#         s = j*i
#         print('%dx%d=%d'%(i,j,s),end=' ')
#         i = i + 1
#     print(' ')
# i=0
# j=0
# while i<9:
#     i+=1
#     while j<9:
#         j+=1
#         print(j,"x",i,"=",i*j,"\t",end="")
#         if i==j:
#             j=0
#             print("\t")
#             #等价print("")
#             break
import time
#! /usr/bin/python
# _*_ coding:UTF-8 _*_
myDict={1:'a',2:'b'}
print(dict.items(myDict))#dict_items([(1, 'a'), (2, 'b')])
for key,value in dict.items(myDict):
    print(key,value)
    time.sleep(1)
list=[1,2,3,4]
for i in range(len(list)):
    print(list[i])
    time.sleep(1)
#.....集合，元组..。
#时间的格式化
print('当前时间未格式化',time.localtime(time.time()))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
time.sleep(1)
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# 类似斐波那契数列12 specifies the minimum width of the field, meaning the output will be padded with spaces on the left if the number is shorter than 12 characters.
# ld indicates that the variable is a long integer.
f1=f2=1
for i in range(1,22):
    print('%12ld %12ld'%(f1,f2))
    if(i%3)==0:
        print('')
    f1=f1+f2
    f2=f1+f2
#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#递归做，非常慢。计算n=36就要大概七八秒吧
def fib(n):
    if n==1 or n==2:
        return 1
    else:
        return fib(n-1)+fib(n-2)
print (fib(36))
h = 0
leap = 1
from math import sqrt
from sys import stdout
for m in range(101,201):
    k = int(sqrt(m + 1))
    for i in range(2,k + 1):
        if m % i == 0:
            leap = 0
            break
    if leap == 1:
        # printed with a minimum width of 4 characters
        print ('%-4d' % m)
        h += 1
        if h % 10 == 0:
            print ('')
    leap = 1
print ('The total is %d' % h)
