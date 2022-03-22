#
# @lc app=leetcode.cn id=47 lang=python3
#
# [47] 全排列 II
#

# @lc code=start
class Solution:
    def dfs(self,nums,res,cur,visited):
        if len(cur) == len(nums):
            res.append(cur[:])
            return
        for i in range(len(nums)):
            #去重操作:已经访问过了|重复元素保证从左向右进行访问
            if visited[i] or (i>0 and nums[i-1]==nums[i] and not visited[i-1]): 
                continue
            # if i in visited:
            #     continue
            # # 增加条件(i-1) not in visited
            # # 如果重复元素集合中前部分还没有元素被访问,则后部分元素也不会被访问
            # if i>0 and nums[i-1]==nums[i] and (i-1) not in visited:
            #     continue
            cur.append(nums[i])
            visited[i]=1
            # visited.add(i)
            self.dfs(nums,res,cur,visited)
            cur.pop()
            visited[i]=0
            # visited.remove(i)
        return

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums = sorted(nums)
        res = []
        cur = []
        visited = [0 for i in range(len(nums))]
        # visited = set()
        self.dfs(nums,res,cur,visited)
        return res

# @lc code=end

