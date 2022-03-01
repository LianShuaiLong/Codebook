#
# @lc app=leetcode.cn id=213 lang=python3
#
# [213] 打家劫舍 II
#

# @lc code=start
class Solution:
    #将整个数组拆成[0:len(nums)-1]和[1:len(nums)]两个子数组
    #然后在两个子数组中进行“隔一”偷盗(即打家劫舍I)即可
    # [1,2,3,4]不能同时偷1和4,
    # [1,2,3]可以同时偷1和3,[2,3,4]可以同时偷2和4
    def rob(self, nums: List[int]) -> int:
        if len(nums)==1:
            return nums[0]
        if len(nums)==2:
            return max(nums[0],nums[1])
        nums_1 = nums[0:(len(nums)-1)]
        nums_2 = nums[1:len(nums)]
        dp_1=[]
        max_rob1 = 0
        if len(nums_1)==1:
            max_rob1 = nums_1[0]
        elif len(nums_1)==2:
            max_rob1 = max(nums_1[0],nums_1[1])
        else:
            dp_1.append(nums_1[0])
            dp_1.append(max(nums_1[0],nums_1[1]))
            for i in range(2,len(nums_1)):
                rob_1 = dp_1[i-2]+nums_1[i]
                rob_2 = dp_1[i-1]
                max_rob1 = max(rob_1,rob_2)
                dp_1.append(max_rob1)
        dp_2=[]
        max_rob2 = 0
        if len(nums_2)==1:
            max_rob2 = nums_2[0]
        elif len(nums_2)==2:
            max_rob2 = max(nums_2[0],nums_2[1])
        else:
            dp_2.append(nums_2[0])
            dp_2.append(max(nums_2[0],nums_2[1]))
            for i in range(2,len(nums_2)):
                rob_1 = dp_2[i-2]+nums_2[i]
                rob_2 = dp_2[i-1]
                max_rob2 = max(rob_1,rob_2)
                dp_2.append(max_rob2)
        return max(max_rob1,max_rob2)
        
# @lc code=end

