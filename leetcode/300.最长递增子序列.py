#
# @lc app=leetcode.cn id=300 lang=python3
#
# [300] 最长递增子序列
#

# @lc code=start
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # 动态规划,动态规划核心是如何定义状态,根据题目考虑
        # 将最长递增子序列的长度定位状态,但是此时状态转移方程
        # 不方便写;基于方便写出状态转移方程，可以将状态定义为
        # 以该元素结尾的最长递增子序列长度，此时状态转移方程就
        # 很容易写出来
        # dp[i]用来保存以nums[i]为结尾的最长递增子序列
        if len(nums) == 1:
            return 1
        dp = [1]
        for i in range(1,len(nums)):
            new_length = 1
            for j in range(0,i):#注意这里要从idx=0开始比较
                if nums[i]>nums[j]:
                    new_length = max(dp[j]+1,new_length)
            dp.append(new_length)
        return max(dp)
        # 待补充，优化解:Nlog(N)的时间复杂度

# @lc code=end

