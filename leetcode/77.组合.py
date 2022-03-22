#
# @lc app=leetcode.cn id=77 lang=python3
#
# [77] 组合
#

# @lc code=start
class Solution:
    def dfs(self,n,k,res,cur,begin):
        if len(cur) == k:
            res.append(cur[:])
            return
        else:
            for i in range(begin,n):
                cur.append(i+1)
                self.dfs(n,k,res,cur,i+1)
                cur.pop()
            return
        
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        cur = []
        # 组合数不用设置visited,排列数需要设置visited,
        # 组合数需要设置begin,而排列数每次都是从0开始遍历
        # 有重复数的话,需要根据sort之后根据
        # i>0 and num[i-1]==num[i]找重复数,进而定位下一个起始位
        self.dfs(n,k,res,cur,0)
        return res
# @lc code=end

