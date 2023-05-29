#
# @lc app=leetcode.cn id=118 lang=python3
#
# [118] 杨辉三角
#

# @lc code=start
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        if numRows==0:
            return []
        if numRows==1:
            return [[1]]
        res = [[1]]
        for i in range(1,numRows):
            cur = []
            cur.append(1)
            for j in range(1,i):
                v = res[-1][j-1]+res[-1][j]
                cur.append(v)
            cur.append(1)
            res.append(cur)
        return res

# @lc code=end

