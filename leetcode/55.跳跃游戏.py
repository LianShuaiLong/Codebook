#
# @lc app=leetcode.cn id=55 lang=python3
#
# [55] 跳跃游戏
#

# @lc code=start
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_loc = 0
        for i in range(len(nums)):
            cur_loc = i+nums[i]
            # 注意这个判断条件
            # 1.当前位置得可以到达
            # 2.从当前开始到达最远得位置大于目前最远能到达的位置
            if i<=max_loc and cur_loc>max_loc:
                max_loc = cur_loc
        return max_loc>=len(nums)-1
# @lc code=end

