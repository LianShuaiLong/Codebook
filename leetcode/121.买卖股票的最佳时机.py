#
# @lc app=leetcode.cn id=121 lang=python3
#
# [121] 买卖股票的最佳时机
#

# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # 遍历一次,每次维护到当前最低价格，最大利润
        # 运行到当前，不用遍历之前所有价格，只需要知道之前最低价格即可
        if len(prices)<=1:
            return 0
        min_price = prices[0]
        max_profit = 0
        for i in range(1,len(prices)):
            max_profit = max(max_profit,prices[i]-min_price)
            min_price = min(min_price,prices[i])
        return max_profit

            
       


# @lc code=end

