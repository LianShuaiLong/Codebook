#
# @lc app=leetcode.cn id=106 lang=python3
#
# [106] 从中序与后序遍历序列构造二叉树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> TreeNode:
        if len(postorder)==0:
            return None
        elif len(postorder)==1:
            root = TreeNode(val=postorder[-1])
            return root
        else:
            val_root = postorder[-1]
            root = TreeNode(val = val_root)
            i = 0
            while i < len(inorder):
                if inorder[i]==val_root:
                    break
                i+=1
            inorder_left = inorder[0:i]
            postorder_left = postorder[0:i]
            inorder_right = inorder[(i+1):len(inorder)]
            #注意这里posterorder的起始idx是i not (i+1)
            postorder_right = postorder[i:(len(postorder)-1)]
            left = self.buildTree(inorder_left,postorder_left)
            right = self.buildTree(inorder_right,postorder_right)
            root.left = left
            root.right = right
            return root
# @lc code=end

