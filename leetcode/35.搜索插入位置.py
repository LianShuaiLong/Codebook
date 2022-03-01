#
# @lc app=leetcode.cn id=35 lang=python3
#
# [35] 搜索插入位置
#

# @lc code=start
class Solution:
    # 分两步考虑：
    # 第一步：target不在列表内部
    #        在表头|表尾 表外
    # 第二部：target在列表内部
    # 需要注意的是1.每次更新left|right的方式，
    # 不能直接left=mid|right=mid，考虑[0,2]\n1
    # 这样会导致left一直在mid的位置，进入死循环
    # 2.while循环的条件，left<=right，
    # 这个是与1的赋值方式对应的，考虑[1,3,4]\n2
    # 3.最后跳出循环，说明right>left，要么是left移到
    # 了right的右侧(target比=位置的数大，位于right~|left|)；
    # 要么是right移到了left的左侧(target比=位置的数小，
    # 位于|right|~left)
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)-1
        val_left = nums[left]
        val_right = nums[right]
        if val_left>=target:
            return 0
        if val_right<target:
            return len(nums)
        if val_right == target:
            return len(nums)-1
        while left<=right:
            val_left = nums[left]
            val_right = nums[right]
            if val_left == target:
                return left
            if val_right == target:
                return right
            mid = (left+right)//2
            val_mid = nums[mid]
            if target == val_mid:
                return mid
            else:
                if val_mid>target:
                    right = mid-1
                else:
                    left = mid+1
        return right+1
# @lc code=end

