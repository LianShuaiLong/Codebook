#
# @lc app=leetcode.cn id=27 lang=python3
#
# [27] 移除元素
#

# @lc code=start
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        num_repeat = 0
        for num in nums:
            if num==val:
                num_repeat+=1
        right = len(nums)-1
        #注意这个范围:len(nums)-num_repeat
        for i in range(len(nums)-num_repeat):
            if nums[i]== val:
                while right>0 and nums[right]==val:
                    right-=1
                tmp = nums[i]
                nums[i] = nums[right]
                nums[right] = tmp
        return len(nums)-num_repeat

# @lc code=end

