#
# @lc app=leetcode.cn id=198 lang=python3
#
# [198] 打家劫舍
#

# @lc code=start
class Solution:
    # 状态：到目前id_舍,能偷盗金额的最大值
    # 初始化：只有一家的时候，只能偷一家；有两家的时候，挑有钱的偷
    # 状态转移：到目前id_舍，要么前一家已经偷了，此家不能偷；
    # 要么前一家没有偷，这一家可以偷，偷盗的最大金额为前一家之前最大金额加这一家金额
    def rob(self, nums: List[int]) -> int:
        if len(nums)==1:
            return nums[0]
        if len(nums)==2:
            return max(nums)
        dp = []
        dp.append(nums[0])
        dp.append(max(nums[0],nums[1]))
        for i in range(2,len(nums)):
            max_rob = max(dp[i-2]+nums[i],dp[i-1])
            dp.append(max_rob)
        return dp[-1]
# @lc code=end

