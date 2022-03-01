#
# @lc app=leetcode.cn id=63 lang=python3
#
# [63] 不同路径 II
#

# @lc code=start
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        matrix = [[0 for i in range(n)] for j in range(m)]
        if obstacleGrid[0][0]==1:
            return 0
        else:
            matrix[0][0] = 1
        for i in range(1,m):
            if obstacleGrid[i][0]==1:
                matrix[i][0] = 0
            else:
                matrix[i][0] = matrix[i-1][0]
        for i in range(1,n):
            if obstacleGrid[0][i]==1:
                matrix[0][i] = 0
            else:
                matrix[0][i] = matrix[0][i-1]
        for i in range(1,m):
            for j in range(1,n):
                if obstacleGrid[i][j]==1:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = sum([matrix[i-1][j],matrix[i][j-1]])
        return matrix[m-1][n-1]
# @lc code=end

