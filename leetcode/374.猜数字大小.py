#
# @lc app=leetcode.cn id=374 lang=python3
#
# [374] 猜数字大小
#

# @lc code=start
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber_help(self,lower:int,higher:int)->int:
        while lower<higher:
            if guess(lower) == 0:
                return lower
            if guess(higher) == 0:
                return higher
            mid = (lower+higher)//2
            if guess(mid) == 0:
                return mid
            else:
                if guess(mid)==-1:
                    higher = mid-1
                else:
                    lower = mid+1
        return lower

    def guessNumber(self, n: int) -> int:
        return self.guessNumber_help(1,n)
        
# @lc code=end

