#
# @lc app=leetcode.cn id=96 lang=python3
#
# [96] 不同的二叉搜索树
#

# @lc code=start
class Solution:
    def numTrees(self, n: int) -> int:
        if n<2:
            return 1
        dp = [0 for i in range(n+1)]
        dp[0] = 1 
        dp[1] = 1
        dp[2] = 2
        for i in range(3,n+1):
            #root结点的取值[1,i],j是当前root结点取值
            #左子树的所有结点范围是[1,j-1] j-1<i
            #右子树的所有结点范围是[j+1,i],统一减j,
            #右子树的所有结点范围是[1,i-j] i-j<i
            #可以使用动态规划
            for j in range(1,i+1):
                tree_num = dp[j-1]*dp[i-j]
                dp[i]+=tree_num
        return dp[-1]

# @lc code=end

