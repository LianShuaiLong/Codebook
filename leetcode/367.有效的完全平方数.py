#
# @lc app=leetcode.cn id=367 lang=python3
#
# [367] 有效的完全平方数
#

# @lc code=start
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        left = 1 
        right = num
        if left*left == num or right*right == num:
            return True
        # 这里的判断条件不能是<=,如果有=而且最终mid*mid>num且right=mid
        # 则会陷入死循环
        while left<right:
            if left*left == num:
                return True
            if right*right == num:
                return True
            mid = (left+right)//2
            if mid*mid == num:
                return True
            else:
                if mid*mid<num:
                    left = mid+1
                else:
                    right = mid
        return False
# @lc code=end

