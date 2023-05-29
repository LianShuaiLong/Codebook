#
# @lc app=leetcode.cn id=7 lang=python3
#
# [7] 整数反转
#

# @lc code=start
class Solution:
    def reverse(self, x: int) -> int:
        ele_list = []
        if x>=0:
            t = x
        else:
            t = -x
        while t>0:
            yushu = t%10
            t = t//10
            ele_list.append(yushu)
        res = 0
        for ele in ele_list:
            res=res*10+ele
        if res>pow(2,31)-1 or res<-pow(2,31):
            return 0
        if x>=0:
            return res
        else:
            return -res

# @lc code=end

