#
# @lc app=leetcode.cn id=48 lang=python3
#
# [48] 旋转图像
#

# @lc code=start
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        #注意切片操作是针对np数组,list没有这个特性
        n = len(matrix)
        num_layer = n//2
        for i in range(num_layer):
            i_columns_1 = []
            for j in range(i,n-i):
                i_columns_1.append(matrix[i][j])
            #print(i_columns_1)
            i_rows_1 = []
            for j in range(i,n-i):
                i_rows_1.append(matrix[j][n-1-i])
            #print(i_rows_1)
            i_columns_2 = []
            for j in range(n-1-i,i-1,-1):
                i_columns_2.append(matrix[n-1-i][j])
            #print(i_columns_2)
            i_rows_2 = []
            for j in range(n-1-i,i-1,-1):
                i_rows_2.append(matrix[j][i])
            #print(i_rows_2)
            for j in range(i,n-i):
                matrix[i][j] = i_rows_2[j-i]
            for j in range(i,n-i):
                matrix[j][n-1-i] = i_columns_1[j-i]
            #注意这里i_rows_i idx的取值
            for j in range(n-1-i,i-1,-1):
                matrix[n-1-i][j] = i_rows_1[(n-1-i)-j]
            for j in range(n-1-i,i-1,-1):
                matrix[j][i] = i_columns_2[(n-1-i)-j]
        
        return
# @lc code=end

