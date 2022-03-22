#
# @lc app=leetcode.cn id=90 lang=python3
#
# [90] 子集 II
#

# @lc code=start
class Solution:
    def dfs(self,nums,res,cur,k,begin):
        if len(cur)== k:
            res.append(cur[:])
            return
        else:
            for i in range(begin,len(nums)):
                if i>begin and nums[i-1]==nums[i]:
                    continue
                cur.append(nums[i])
                self.dfs(nums,res,cur,k,i+1)
                cur.pop()
            return
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        m = len(nums)
        #只有这里进行排序之后,后面去重操作中的nums[i-1]==nums[i]才有意义
        nums = sorted(nums)
        res = []
        cur = []
        begin = 0
        res.append([])
        for k in range(1,m):
            self.dfs(nums,res,cur,k,begin)
        res.append(nums)
        return res
# @lc code=end

