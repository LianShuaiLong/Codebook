#
# @lc app=leetcode.cn id=53 lang=python3
#
# [53] 最大子数组和
#

# @lc code=start
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # 定义状态
        # dp[i]以当前元素结尾的连续子数组的最大和
        dp = []
        dp.append(nums[0])
        max_num = nums[0]
        for i in range(1,len(nums)):
            num = max(dp[i-1]+nums[i],nums[i])
            dp.append(num)
            max_num = max(max_num,num)
        return max_num

# @lc code=end

