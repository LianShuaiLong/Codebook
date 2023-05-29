#
# @lc app=leetcode.cn id=119 lang=python3
#
# [119] 杨辉三角 II
#

# @lc code=start
class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        if rowIndex==0:
            return [1]
        res = [[1]]
        for i in range(1,rowIndex+1):
            cur = []
            cur.append(1)
            for j in range(1,i):
                v = res[-1][j-1]+res[-1][j]
                cur.append(v)
            cur.append(1)
            res.append(cur)
        return res[-1]
        #优化，采用滚动数据，注意杨辉三角每一行的数的个数与其所在行数相等
        #也就是说O(rowIndex)的空间复杂度可以转换为只存储当前rowIndex行里得数


# @lc code=end

