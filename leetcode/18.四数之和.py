#
# @lc app=leetcode.cn id=18 lang=python3
#
# [18] 四数之和
#

# @lc code=start
class Solution:
    def sort(self,nums):
        n = len(nums)
        if n==0:
            return 
        if n==1:
            return nums
        mid = n//2
        left = self.sort(nums[0:mid])
        right = self.sort(nums[mid:n])
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

    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        if n<4:
            return []
        new_nums = self.sort(nums)
        i=0
        exist_ = set()
        res = []
        while i<=n-4:
            val_i = new_nums[i]
            #注意这里也要有一层循环
            for j in range(i+1,n-2):
                val_j = new_nums[j]
                left = j+1
                right = n-1
                while left<right:
                    val_left = new_nums[left]
                    val_right = new_nums[right]
                    cur_sum = val_i+val_j+val_left+val_right
                    if cur_sum==target:
                        #有没有去重的好方式
                        cur_list = f'{val_i}{val_j}{val_left}{val_right}'
                        if len(exist_)==0 or cur_list not in exist_:
                            res.append([val_i,val_j,val_left,val_right])
                            exist_.add(cur_list)
                        left+=1
                        right-=1
                    elif cur_sum<target:
                        left+=1
                    else:
                        right-=1
            i+=1
        return res
# @lc code=end

