#
# @lc app=leetcode.cn id=78 lang=python3
#
# [78] 子集
#

# @lc code=start
class Solution:
    def dfs(self,nums,res,cur,k,begin):
        if len(cur)==k:
            res.append(cur[:])
            return
        else:
            for i in range(begin,len(nums)):
                cur.append(nums[i])
                self.dfs(nums,res,cur,k,i+1)
                cur.pop()
            return
    def subsets(self, nums: List[int]) -> List[List[int]]:
        #组合数的升级版,只是这次k的取值范围是0-len(nums)
        n = len(nums)
        res = []
        res.append([])
        for i in range(1,n):
            cur = []
            self.dfs(nums,res,cur,i,begin=0)
        res.append(nums)
        return res

# @lc code=end

