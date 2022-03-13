#
# @lc app=leetcode.cn id=134 lang=python3
#
# [134] 加油站
#

# @lc code=start
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        #暴力求解法:找到第一个gas_left>=0的位置，然后进行判断
        # gas_left = []
        # for i in range(len(gas)):
        #     gas_left.append(gas[i]-cost[i])
        # for i in range(len(gas_left)):
        #     if gas_left[i]>=0:
        #         sum_i = 0
        #         for j in range(len(gas_left)+1):
        #             j_t = i+j
        #             j_t = j_t%len(gas_left)
        #             sum_i+=gas_left[j_t]
        #             if sum_i<0:
        #                 break
        #         if sum_i>=0:
        #             return i
        # return -1
        # 上述会超时，进行优化，如果从i出发，最远到达j
        # 那么从i-j之间任意一点出发均不能绕一周，分析：
        # 假设i+1出发可以绕一周，同时i也可以到达i+1,那么
        # 就说明从i出发也是可以绕一周的，前后矛盾
        i=0
        while i < len(gas):
            j = i
            gas_remain = gas[i]
            while gas_remain-cost[j]>=0:
                gas_remain = gas_remain-cost[j]+gas[(j+1)%len(gas)]
                j = (j+1)%len(gas)
                if j==i:
                    return i
            #这种情况是j在i前面，若这时候从j+1开始可以绕一周，则说明到i之前就已经return了
            if j<i:
                return -1
            i=j+1 #注意这里应该从j+1开始算，前面是说最远到达位置是j
        return -1
                
            
# @lc code=end

