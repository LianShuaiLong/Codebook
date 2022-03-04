#
# @lc app=leetcode.cn id=145 lang=python3
#
# [145] 二叉树的后序遍历
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        if not root.left and not root.right:
            return [root.val]
        res = []
        if root.left:
            node_left = self.postorderTraversal(root.left)
            res.extend(node_left)
        if root.right:
            node_right = self.postorderTraversal(root.right)
            res.extend(node_right)
        res.append(root.val)
        return res
# @lc code=end

