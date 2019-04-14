# var = 'Hello workld'
# var2 = "Runoob"

# print("var1[0]", var[0])
# print("var2[1:5]", var2[1:5] + 'Runnob')

# #!/usr/bin/python3
 
# print ("我叫 %s 今年 %d 岁!" % ('小明', 10))



# print([False])

# class Equip:
#     equiptest = 1
#     def fire(self):
#         print('fire skill')

# class Riven:
#     camp = 'Noxus'
#     def __init__(self, nickname):
#         self.nickname = nickname
#         self.equip = Equip()

# r1 = Riven('rvv')
# e1 = Equip()
# e2 = Equip()
# e2.equiptest = 4
# Equip.equiptest = 10

# e2.equiptest = 6
# r1.equip.fire()
from typing import List

class Solution:
    def numEnclaves(self, A: List[List[int]]) -> int:
        """
        从四个边缘开始dfs，当前点如果是1，置为-1，上下左右如果有是1的，则加入栈中继续迭代下去
        最后计算四个非边缘中有多少个一
        """ 
        def dfs(line_row, line_col):
            stack = [(line_row, line_col)]
            while stack:
                temp_row, temp_col = stack.pop()
                A[temp_row][temp_col] = -1
                if temp_row - 1 >= 0:
                    if A[temp_row - 1][temp_col] == 1:
                        stack.append((temp_row - 1, temp_col))
                if temp_col - 1 >= 0:
                    if A[temp_row][temp_col - 1] == 1:
                        stack.append((temp_row, temp_col - 1))
                if temp_row + 1 < row:
                    if A[temp_row + 1][temp_col] == 1:
                        stack.append((temp_row + 1, temp_col))
                if temp_col + 1 < col:
                    if A[temp_row][temp_col + 1] == 1:
                        stack.append((temp_row, temp_col + 1))

        row = len(A)
        col = len(A[0])

        for i in range(row):
            if A[i][0] == 1:
                dfs(i, 0)
            if A[i][col - 1] == 1:
                dfs(i, col - 1)
        for i in range(col):
            if A[0][i] == 1:
                dfs(0, i)
            if A[row - 1][i] == 1:
                dfs(row - 1, i)
        res = 0
        for i in range(1, row - 1):
            res += A[i].count(1)
        return res

s1 = Solution()
arry = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[1,0,1,1]]
o1 = s1.numEnclaves(arry)
print('result is ',o1)