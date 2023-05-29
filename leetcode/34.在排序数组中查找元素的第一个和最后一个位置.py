#
# @lc app=leetcode.cn id=34 lang=python3
#
# [34] 在排序数组中查找元素的第一个和最后一个位置
#

# @lc code=start
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if len(nums)==0:
            return [-1,-1]
        left = 0
        right = len(nums)-1
        if target<nums[0] or target>nums[-1]:
            return [-1,-1]
        else:
            while left<=right:
                mid = (left+right)//2
                val_left = nums[left]
                val_right = nums[right]
                val_mid = nums[mid]
                if val_left == target:
                    i_left,i_right = left,left
                    #注意这里要保证i_left/i_right有效
                    while i_left>=0 and nums[i_left] == target:
                        i_left-=1
                    while i_right<len(nums) and nums[i_right] == target:
                        i_right+=1
                    return [i_left+1,i_right-1]
                elif val_right == target:
                    i_left,i_right = right,right
                    while  i_left>=0 and nums[i_left] == target:
                        i_left-=1
                    while i_right<len(nums) and nums[i_right] == target:
                        i_right+=1
                    return [i_left+1,i_right-1]
                else:
                    if val_mid == target:
                        i_left,i_right = mid,mid
                        while i_left>=0 and nums[i_left] == target:
                            i_left-=1
                        while i_right<len(nums) and nums[i_right] == target:
                            i_right+=1
                        return [i_left+1,i_right-1]
                    elif val_mid>target:
                        right = mid-1
                    else:
                        left = mid+1
            return [-1,-1]

# @lc code=end

