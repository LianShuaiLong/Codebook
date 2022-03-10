#
# @lc app=leetcode.cn id=15 lang=python3
#
# [15] 三数之和
#

# @lc code=start
class Solution:
    def sort(self,nums):
        if len(nums)==0:
            return
        if len(nums)==1:
            return nums
        mid = len(nums)//2
        left = self.sort(nums[0:mid])
        right = self.sort(nums[mid:len(nums)])
        i,j=0,0
        res = []
        while i<len(left) and j<len(right):
            val_left = left[i]
            val_right = right[j]
            if val_left<val_right:
                res.append(val_left)
                i+=1
            else:
                res.append(val_right)
                j+=1
        if i<len(left):
            res.extend(left[i:len(left)])
        if j<len(right):
            res.extend(right[j:len(right)])
        return res
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums)<3:
            return []
        new_nums = self.sort(nums)
        # print(new_nums)
        i = 0
        res = []
        exist_=set()
        while i<len(new_nums):
            a = new_nums[i]
            left = i+1
            right = len(nums)-1
            while left<right:
                val_left = new_nums[left]
                val_right = new_nums[right]
                if val_left+val_right+a == 0:
                    if len(exist_)==0 or f'{a}-{val_left}-{val_right}' not in exist_:
                        res.append([a,val_left,val_right])
                        exist_.add(f'{a}-{val_left}-{val_right}')
                    left+=1
                    right-=1
                elif val_left+val_right+a>0:
                    right-=1
                else:
                    left+=1
            i+=1
        return res

# @lc code=end

