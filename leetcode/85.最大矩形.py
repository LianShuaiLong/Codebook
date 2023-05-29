#
# @lc app=leetcode.cn id=85 lang=python3
#
# [85] 最大矩形
#

# @lc code=start
class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        #有一个变量存储当前最大的矩形面积
        #状态:以当前点为右下角的矩形
        #转移方程[i,j],[i-1,j],[i,j-1]最大x,最大j
        max_Rec = 0
        state_matrix = [[(i,j) for j in range(n)] for i in range(m)]
        if matrix[0][0]=="0":
            state_matrix[0][0]=(1,1)
            max_Rec = 0
        else:
            state_matrix[0][0]=(0,0)
            max_Rec = 1
        for i in range(1,m):
            if matrix[i][0]=="0":
                state_matrix[i][0]=(i+1,1)
                Rec = 0
            else:
                state_matrix[i][0]=(state_matrix[i-1][0][0],0)
                Rec = i+1-state_matrix[i-1][0][0]
            max_Rec = max(max_Rec,Rec)
        for i in range(1,n):
            if matrix[0][i]=="0":
                state_matrix[0][i]=(1,i+1)
                Rec = 0
            else:
                state_matrix[0][i]=(0,state_matrix[0][i-1][1])
                Rec = i+1-state_matrix[0][i-1][1]
            max_Rec = max(max_Rec,Rec)
        for i in range(1,m):
            for j in range(1,n):
                if matrix[i][j]=="1":
                    if matrix[i-1][j-1]=="1":
                        new_x = max(state_matrix[i-1][j-1][0],state_matrix[i-1][j][0])
                        new_y = max(state_matrix[i-1][j-1][1],state_matrix[i][j-1][1])
                        state_matrix[i][j] = (new_x,new_y)
                        Rec = (i+1-new_x)*(j+1-new_y)
                        max_Rec = max(max_Rec,Rec)
                    else:
                        Rec1 = (i+1-state_matrix[i-1][j][0])
                        Rec2 = (j+1-state_matrix[i][j-1][1])
                        if Rec2>Rec1:
                            state_matrix[i][j] =(i,state_matrix[i][j-1][1]) 
                            max_Rec = max(max_Rec,Rec2)
                        else:
                            state_matrix[i][j] = (state_matrix[i-1][j][0],j)
                            max_Rec = max(max_Rec,Rec2)
                else:
                    state_matrix[i][j]=(i+1,j+1)  
        return max_Rec

# @lc code=end

