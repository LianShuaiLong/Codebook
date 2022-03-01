#
# @lc app=leetcode.cn id=162 lang=python3
#
# [162] 寻找峰值
#

# @lc code=start
class Solution:
    # 如果mid的值严格大于mid+1的值
    # 则在<=mid的区域一定有一个局部极大值
    # 如果mid的值严格小于mid+1的值
    # 则在>mid的区域一定有一个局部极大值
    # 把题目改成寻找极大值更合适
    def findPeakElement(self, nums: List[int]) -> int:
        if len(nums)==1:
            return 0
        left = 0
        right = len(nums)-1
        while left<right:
            mid = (left+right)//2
            if nums[mid]>nums[mid+1]:
                right = mid
            else:
                left = mid+1
        return left
      
# @lc code=end

