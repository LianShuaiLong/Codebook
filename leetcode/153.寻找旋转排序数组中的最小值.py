#
# @lc app=leetcode.cn id=153 lang=python3
#
# [153] 寻找旋转排序数组中的最小值
#

# @lc code=start
class Solution:
    def findMin(self, nums: List[int]) -> int:
        # 直接二分查找
        left = 0
        right = len(nums)-1
        while left<=right:
            val_left = nums[left]
            val_right = nums[right]
            mid = (left+right)//2
            val_mid = nums[mid]
            if val_left>val_right:
                # 若val_mid>val_right,则旋转点在mid的右边，且不包括mid(mid肯定不是旋转点)
                # 旋转点最起码要满足val_idx<val_right
                if val_mid>val_right:
                    left = mid+1
                else:
                    # 注意right的取值,是mid而不是mid-1
                    # 若val_mid<val_right，则旋转点应该在mid的左边，且包括mid
                    # 因为val_mid是满足小于val_right的
                    right = mid
            else:
                return nums[left]
        return nums[left]

                

# @lc code=end

