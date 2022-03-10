#
# @lc app=leetcode.cn id=45 lang=python3
#
# [45] 跳跃游戏 II
#

# @lc code=start
class Solution:
    def jump(self, nums: List[int]) -> int:
        #记录当前位置最远能到达位置和最小跳跃次数
        # 会超时
        # loc_jump = []
        # min_jump = len(nums)-1
        # for i in range(len(nums)):
        #     loc = i+nums[i]
        #     if i==0:
        #         jump = 0
        #     else:
        #         jump = loc_jump[i-1][1]+1
        #     for j in range(0,i):
        #         if loc_jump[j][0]>=i:
        #             jump = min(jump,loc_jump[j][1]+1)
        #     if loc>=len(nums)-1:
        #         #注意这里的jump是到当前位置的jump次数，到最后还需要+1
        #         min_jump = min(min_jump,jump+1)
        #     loc_jump.append([loc,jump])
        # return min_jump
        # 相当于将上述代码点对点的平移变成了区间到区间的平移
        # 每次区间平移即完成一次jump+1操作
        # 注意长度为1的情况，后面的代码默认长度大于1
        if len(nums)==1:
            return 0
        left = 1
        right = nums[0]
        jump = 1
        while right<len(nums)-1:
            new_right = right
            for i in range(left,right+1):
                new_right = max(i+nums[i],new_right)
            #此处jump表示跳到新的[left,right]区间，所需要的jump数
            jump+=1
            left = right+1
            right = new_right
        return jump
            
                
# @lc code=end

