#
# @lc app=leetcode.cn id=72 lang=python3
#
# [72] 编辑距离
#

# @lc code=start
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)
        m = m+1
        n = n+1
        matrix = [[0 for i in range(n)] for j in range(m)]
        for i in range(m):
            matrix[i][0] = i
        for i in range(n):
            matrix[0][i] = i
        # word2 向 word1靠拢
        for i in range(1,m):
            for j in range(1,n):
                if word1[i-1] == word2[j-1]:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    #若两者不相等
                    #添加操作
                    add_op = matrix[i-1][j]+1
                    #删除操作(删除此时较长字符串最后一个,然后补上另外一个字符串的最后一个字符)
                    delete_op = matrix[i][j-1]+1
                    #交换操作(直接将一个字符串最后一个字符置成两外一个字符串最后一个字符串)
                    swap_op = matrix[i-1][j-1]+1
                    matrix[i][j] = min(add_op,delete_op,swap_op)
        return matrix[m-1][n-1]
# @lc code=end

