#
# @lc app=leetcode.cn id=122 lang=python3
#
# [122] 买卖股票的最佳时机 II
#

# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # 注意是可以多次买卖
        # 思路:找到数组内部多个先后的递增子序列
        if len(prices)==0:
            return 0
        max_profit = 0
        for i in range(1,len(prices)):
            max_profit=max_profit+prices[i]-prices[i-1]  if prices[i]-prices[i-1]>0 else max_profit
        return max_profit

# @lc code=end

