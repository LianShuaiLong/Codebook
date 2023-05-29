#
# @lc app=leetcode.cn id=41 lang=python3
#
# [41] 缺失的第一个正数
#

# @lc code=start
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        if len(nums)==0:
            return 1
        # 原地hash
        # 第一个缺失的数肯定位于[1,N+1]
        # 遍历数组,将数字放到其应在的索引上面1放到0,2放到1
        # 注意考虑重复数字出现的情况
        for i in range(len(nums)):
            #注意这里，要将“所有i位置的数”都放到其对应的位置，除非该位置的数不在[1,N]
            #均摊复杂度分析
            #注意nums[i]的取值，只要保证nums[i]-1在[0,N-1]即可，最后一个条件是核心
            #前面的两个条件是辅助
            while nums[i]>0 and nums[i]<=len(nums) and nums[nums[i]-1]!=nums[i]:
                nums[nums[i]-1],nums[i] = nums[i],nums[nums[i]-1]
        for i in range(len(nums)):
            if nums[i]-1!=i:
                return i+1
        return len(nums)+1

        
# @lc code=end

