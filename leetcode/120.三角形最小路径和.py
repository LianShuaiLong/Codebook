#
# @lc app=leetcode.cn id=120 lang=python3
#
# [120] 三角形最小路径和
#
# https://leetcode-cn.com/problems/triangle/description/
#
# algorithms
# Medium (68.46%)
# Likes:    968
# Dislikes: 0
# Total Accepted:    210.3K
# Total Submissions: 307.2K
# Testcase Example:  '[[2],[3,4],[6,5,7],[4,1,8,3]]'
#
# 给定一个三角形 triangle ，找出自顶向下的最小路径和。
# 
# 每一步只能移动到下一行中相邻的结点上。相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1
# 的两个结点。也就是说，如果正位于当前行的下标 i ，那么下一步可以移动到下一行的下标 i 或 i + 1 。
# 
# 
# 
# 示例 1：
# 
# 
# 输入：triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
# 输出：11
# 解释：如下面简图所示：
# ⁠  2
# ⁠ 3 4
# ⁠6 5 7
# 4 1 8 3
# 自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。
# 
# 
# 示例 2：
# 
# 
# 输入：triangle = [[-10]]
# 输出：-10
# 
# 
# 
# 
# 提示：
# 
# 
# 1 
# triangle[0].length == 1
# triangle[i].length == triangle[i - 1].length + 1
# -10^4 
# 
# 
# 
# 
# 进阶：
# 
# 
# 你可以只使用 O(n) 的额外空间（n 为三角形的总行数）来解决这个问题吗？
# 
# 
#

# @lc code=start
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        depth = len(triangle)
        if depth==1:
            return triangle[0][0]
        path_sum = []
        path_sum.append(triangle[0])
        for i in range(1,depth):
            cur_layer_len = i+1
            for j in range(cur_layer_len):
                if j==0:
                    path_len = path_sum[i-1][0]+triangle[i][0]
                    path_sum.append([path_len])
                elif j==cur_layer_len-1:
                    path_len = path_sum[i-1][-1]+triangle[i][cur_layer_len-1]
                    path_sum[i].append(path_len)
                else:
                    path_len = min(path_sum[i-1][j-1],path_sum[i-1][j])+triangle[i][j]
                    path_sum[i].append(path_len)
        return min(path_sum[-1])
                
# @lc code=end

