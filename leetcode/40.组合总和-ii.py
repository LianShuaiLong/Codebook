#
# @lc app=leetcode.cn id=40 lang=python3
#
# [40] 组合总和 II
#

# @lc code=start
class Solution:
    def dfs(self,candidates,res,cur,begin,target):
        if target==0:
            res.append(cur[:])
            return
        if begin>=len(candidates):
            return
        for i in range(begin,len(candidates)):
            #在该层循环中，去掉后续重复的情况(不只是与当前有相同的begin)
            # 例如排完序之后的数组是[1,1,1,1,3,3,5],找到第一个1做begin的cur之后
            # 在该层循环中我们需要找到另外一个符合条件的cur,condidates[begin]和candidates[i-1]
            # 都可以找到第一个3，然后dfs完当前cur,需要找下一个，这时候第二个3要用candidates[i-1]去重
            #注意这里不是candidates[i]==candidates[begin]
            if i>begin and candidates[i]==candidates[i-1]:
                continue
            if target-candidates[i]>=0:
                cur.append(candidates[i])
                self.dfs(candidates,res,cur,i+1,target-candidates[i])
                cur.pop()
        

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates = sorted(candidates)
        res = []
        cur = []
        begin = 0
        self.dfs(candidates,res,cur,begin,target)
        return res
# @lc code=end

