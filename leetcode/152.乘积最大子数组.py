#
# @lc app=leetcode.cn id=152 lang=python3
#
# [152] 乘积最大子数组
#

# @lc code=start
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        if len(nums)==1:
            return nums[0]
        dp=[]
        dp.append((nums[0],nums[0]))#(当前最大乘积值,当前最小乘积值)
        max_product = nums[0]
        for i in range(1,len(nums)):
            cur_max_value = max(dp[i-1][0]*nums[i],dp[i-1][1]*nums[i],nums[i])
            cur_min_value = min(dp[i-1][0]*nums[i],dp[i-1][1]*nums[i],nums[i])
            dp.append((cur_max_value,cur_min_value))
            max_product = max(max_product,cur_max_value)
        return max_product
# @lc code=end

