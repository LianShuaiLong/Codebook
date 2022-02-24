#
# @lc app=leetcode.cn id=75 lang=python3
#
# [75] 颜色分类
#

# @lc code=start
def quick_sort(nums:list[int],left,right):
    if left>=right:
        return
    i = left
    j = right
    num_benchmark = nums[left]
    while i<j:
        while(i<j and nums[j]>=num_benchmark):
            j-=1
        nums[i] = nums[j]
        while(i<j and nums[i]<=num_benchmark):
            i+=1
        nums[j] = nums[i]
    nums[i] = num_benchmark
    quick_sort(nums,i+1,right)
    quick_sort(nums,left,i-1)
    return
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # 冒泡排序
        # if len(nums)<=1:
        #     return
        # for i in range(len(nums)):
        #     for j in range(1,len(nums)-i):
        #         if nums[j]<nums[j-1]:
        #             tmp = nums[j]
        #             nums[j] = nums[j-1]
        #             nums[j-1] = tmp
        # return
        # 计数排序
        # if len(nums)<=1:
        #     return
        # num_zeros = 0
        # num_ones = 0
        # num_twos = 0
        # for i in range(len(nums)):
        #     if nums[i]==0:
        #         num_zeros+=1
        #     elif nums[i] ==1:
        #         num_ones+=1
        #     else:
        #         num_twos+=1
        # for i in range(num_zeros):
        #     nums[i] = 0
        # for i in range(num_ones):
        #     nums[num_zeros+i] = 1
        # for i in range(num_twos):
        #     nums[num_zeros+num_ones+i]=2
        # return
        # 快速排序 冒泡排序的升级版
        quick_sort(nums,0,len(nums)-1)



# @lc code=end

