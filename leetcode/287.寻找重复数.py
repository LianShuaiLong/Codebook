#
# @lc app=leetcode.cn id=287 lang=python3
#
# [287] 寻找重复数
#

# @lc code=start
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # 抽屉子原理:把10个元素放到9个抽屉子里面,则一定
        # 有一个抽屉子里面放了两个苹果
        # 整体思路(题目已经说明含有重复数字了):
        # 数组长度为n+1,且元素取值范围为[1,n]
        # 设i为[1,n]中的一个数，如果遍历整个数组
        # 小于i的元素个数大于i，则说明重复元素小于i，right=mid
        # 小于i的元素个数小于等于i，重复元素大于i,left = mid+1
        left = 1
        right = len(nums)-1
        while left<right:
            mid = (left+right)//2
            cnt = 0
            # 注意这里要遍历nums数组中所有的元素
            # 与mid进行比较
            for num in nums:
                if num<=mid:
                    cnt +=1
            if cnt>mid:
                right = mid
            else:
                left = mid+1
        return left

# @lc code=end

