#
# @lc app=leetcode.cn id=73 lang=python3
#
# [73] 矩阵置零
#

# @lc code=start
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m = len(matrix)
        n = len(matrix[0])
        n_rows = set()
        n_cols = set()
        for i in range(m):
            for j in range(n):
                if matrix[i][j]==0:
                    n_rows.add(i)
                    n_cols.add(j)
        for i in range(m):
            for j in range(n):
                if i in n_rows or j in n_cols:
                    matrix[i][j]=0
        return 
# @lc code=end

