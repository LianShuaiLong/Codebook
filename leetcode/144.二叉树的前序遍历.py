#
# @lc app=leetcode.cn id=144 lang=python3
#
# [144] 二叉树的前序遍历
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        if not root.left and not root.right:
            return [root.val]
        res = []
        res.append(root.val)
        if root.left:
            node_left = self.preorderTraversal(root.left)
            res.extend(node_left)
        if root.right:
            node_right = self.preorderTraversal(root.right)
            res.extend(node_right)
        return res
# @lc code=end

