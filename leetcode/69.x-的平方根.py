#
# @lc app=leetcode.cn id=69 lang=python3
#
# [69] x 的平方根 
#

# @lc code=start
class Solution:
    # 注意这里求平方根和搜索插入位置的不同
    # 平方根向下取整，搜索插入位置是向上取整
    def mySqrt(self, x: int) -> int:
        left = 0
        right = x
        while left<=right:
            if x==left*left:
                return left
            if x==right*right:
                return right
            mid = (left+right)//2
            if x==mid*mid:
                return mid
            else:
                if mid*mid<x:
                    left = mid+1
                else:
                    right = mid-1
        return right
# @lc code=end

