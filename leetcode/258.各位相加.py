#
# @lc app=leetcode.cn id=258 lang=python3
#
# [258] 各位相加
#

# @lc code=start
class Solution:
    def getnumlist(self,num):
        num_list = []
        while num>0:
            t = num%10
            num_list.append(t)
            num = num//10
        return num_list

    def addDigits(self, num: int) -> int:
        if num==0:
            return 0
        while len(self.getnumlist(num))>1:
            sum = 0
            for n in self.getnumlist(num):
                sum+=n
            num = sum
        return self.getnumlist(num)[0]


# @lc code=end

