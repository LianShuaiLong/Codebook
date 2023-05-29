#
# @lc app=leetcode.cn id=33 lang=python3
#
# [33] 搜索旋转排序数组
#

# @lc code=start
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums)==1:
            if nums[0] == target:
                return 0
            else:
                return -1
        idx_reversed = -1
        #没有发生旋转的情况要单独考虑
        for i in range(len(nums)-1):
            if nums[i]>nums[i+1]:
                idx_reversed = i
                break
        if idx_reversed==-1:
            left_1 = 0
            right_1 = len(nums)-1
            while left_1<=right_1:
                mid = (left_1+right_1)//2
                val_left = nums[left_1]
                val_right = nums[right_1]
                val_mid = nums[mid]
                if val_left == target:
                    return left_1
                elif val_right == target:
                    return right_1
                else:
                    if val_mid==target:
                        return mid
                    elif val_mid>target:
                        right_1 = mid-1
                    else:
                        left_1 = mid+1
            return -1 
        else:
            left_1 = 0
            right_1 = idx_reversed
            left_2 = idx_reversed+1
            right_2 = len(nums)-1
            if target>nums[idx_reversed] or target<nums[left_2]:
                return -1
            if target>=nums[left_1] and target<=nums[right_1]:
                while left_1<=right_1:
                    mid = (left_1+right_1)//2
                    val_left = nums[left_1]
                    val_right = nums[right_1]
                    val_mid = nums[mid]
                    if val_left == target:
                        return left_1
                    elif val_right == target:
                        return right_1
                    else:
                        if val_mid==target:
                            return mid
                        elif val_mid>target:
                            right_1 = mid-1
                        else:
                            left_1 = mid+1
                return -1 
            else:
                # 这个终止条件在结束之后,left和right在同一个位置的情况也判断了
                # 此时left在right的右边
                # 而按照假设，target在right的左边left的右边，
                # 现在left在right的右边，所以肯定不存在
                while left_2<=right_2:
                    mid = (left_2+right_2)//2
                    val_left = nums[left_2]
                    val_right = nums[right_2]
                    val_mid = nums[mid]
                    if val_left == target:
                        return left_2
                    elif val_right == target:
                        return right_2
                    else:
                        if val_mid==target:
                            return mid
                        elif val_mid>target:
                            right_2 = mid-1
                        else:
                            left_2 = mid+1
                return -1
# @lc code=end

