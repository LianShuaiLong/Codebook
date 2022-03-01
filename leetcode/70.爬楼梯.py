#
# @lc app=leetcode.cn id=70 lang=python3
#
# [70] 爬楼梯
#

# @lc code=start
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 0:
            return 0
        if n==1:
            return 1
        if n==2:
            return 2
        dp = [0 for i in range(n)]
        dp[0] = 1
        dp[1] = 2
        for i in range(2,n):
            dp[i] = sum([dp[i-1],dp[i-2]])
        return dp[-1]
# @lc code=end

