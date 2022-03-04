#
# @lc app=leetcode.cn id=111 lang=python3
#
# [111] 二叉树的最小深度
#
# https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/description/
#
# algorithms
# Easy (49.60%)
# Likes:    680
# Dislikes: 0
# Total Accepted:    335.6K
# Total Submissions: 676.2K
# Testcase Example:  '[3,9,20,null,null,15,7]'
#
# 给定一个二叉树，找出其最小深度。
# 
# 最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
# 
# 说明：叶子节点是指没有子节点的节点。
# 
# 
# 
# 示例 1：
# 
# 
# 输入：root = [3,9,20,null,null,15,7]
# 输出：2
# 
# 
# 示例 2：
# 
# 
# 输入：root = [2,null,3,null,4,null,5,null,6]
# 输出：5
# 
# 
# 
# 
# 提示：
# 
# 
# 树中节点数的范围在 [0, 10^5] 内
# -1000 
# 
# 
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def dfs(self,root):
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        elif root.left and not root.right:
            return 1+self.dfs(root.left)
        elif not root.left and root.right:
            return 1+self.dfs(root.right)
        else:
            return 1+min(self.dfs(root.left),self.dfs(root.right))
        
    def minDepth(self, root: TreeNode) -> int:
        return self.dfs(root)
# @lc code=end

