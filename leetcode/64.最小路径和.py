#
# @lc app=leetcode.cn id=64 lang=python3
#
# [64] 最小路径和
#

# @lc code=start
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        matrix = [[0 for i in range(n)] for j in range(m)]
        for i in range(m):
            if i == 0:
                matrix[i][0] = grid[i][0]
            else:
                matrix[i][0] = matrix[i-1][0] + grid[i][0]
        for i in range(n):
            if i == 0:
                matrix[0][i] = grid[0][i]
            else:
                matrix[0][i] = grid[0][i]+matrix[0][i-1]
        for i in range(1,m):
            for j in range(1,n):
                matrix[i][j] = min(matrix[i-1][j],matrix[i][j-1])+grid[i][j]
        return matrix[m-1][n-1]
# @lc code=end

