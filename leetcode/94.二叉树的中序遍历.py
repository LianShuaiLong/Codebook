#
# @lc app=leetcode.cn id=94 lang=python3
#
# [94] 二叉树的中序遍历
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return [] 
        if not root.left and not root.right:
            return [root.val]
        res = []
        if root.left:
            node_left = self.inorderTraversal(root.left)
            res.extend(node_left)
        res.append(root.val)
        if root.right:
            node_right = self.inorderTraversal(root.right)
            res.extend(node_right)
        return res
# @lc code=end

