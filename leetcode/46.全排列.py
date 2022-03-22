#
# @lc app=leetcode.cn id=46 lang=python3
#
# [46] 全排列
#

# @lc code=start
class Solution:
    def dfs(self,nums,res,cur,visited):
        if len(cur)==len(nums):
            res.append(cur[:])
        else:
            for i in range(len(nums)):
                # if i not in visited:
                if not visited[i]:
                    cur.append(nums[i])
                    # visited.add(i)
                    visited[i] = 1
                    self.dfs(nums,res,cur,visited)
                    cur.pop()
                    # visited.remove(i)
                    visited[i] = 0
                else:
                    continue
        return
        
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        cur = []
        # visited = set()
        visited = [0 for i in range(len(nums))]
        self.dfs(nums,res,cur,visited)
        return res
# @lc code=end

