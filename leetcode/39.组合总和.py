#
# @lc app=leetcode.cn id=39 lang=python3
#
# [39] 组合总和
#

# @lc code=start
class Solution:
    #由于每个元素都可以重复利用，所以有两种选择：1.跳过当前元素再开始 2，直接从当前元素开始
    #注意不要每次都从idx=0进行元素选择，这个是组合不是排列，这种操作肯定会重复很多
    def dfs(self,candidates,res,cur,begin,target):
        #该终止条件对1,2都有效
        if target==0:
            res.append(cur[:])
            # cur.pop() 与最后的pop重复
            return
        #该终止条件对于1有效
        if begin>=len(candidates):
            return
        #每一个元素都有两种选择，1.被选多次(>=1) 2.直接不选
        #直接跳过当前元素
        self.dfs(candidates,res,cur,begin+1,target)
        #选择当前元素
        if target-candidates[begin]>=0:
            cur.append(candidates[begin])
            self.dfs(candidates,res,cur,begin,target-candidates[begin])
            # if len(cur)>0:
            #     cur.pop()
            cur.pop()
        return
        

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        if len(candidates)==0:
            return []
        res = []
        cur = []
        begin =0
        self.dfs(candidates,res,cur,begin,target)
        return res
# @lc code=end

