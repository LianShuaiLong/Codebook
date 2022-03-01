#
# @lc app=leetcode.cn id=62 lang=python3
#
# [62] 不同路径
#

# @lc code=start
class Solution:
    # 动态规划要点：
    # 1.定义状态
    # 2.状态初始化
    # 3.状态转移方程
    def uniquePaths(self, m: int, n: int) -> int:
        if m == 0 or n==0:
            return 0
        matrix = [[0 for i in range(n)] for j in range(m)]
        for i in range(m):
            matrix[i][0] = 1
        for i in range(n):
            matrix[0][i] = 1
        for i in range(1,m):
            for j in range(1,n):
                matrix[i][j] = sum([matrix[i-1][j],matrix[i][j-1]])
        return matrix[m-1][n-1]
      
# @lc code=end

