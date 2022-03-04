#
# @lc app=leetcode.cn id=105 lang=python3
#
# [105] 从前序与中序遍历序列构造二叉树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        if len(preorder)==1:
            root = TreeNode(val=preorder[0])
            return root
        elif len(preorder)==0:
            return None
        else:
            val_root = preorder[0]
            i = 0
            while i<len(inorder):
                if inorder[i]==val_root:
                    break
                i+=1
            root = TreeNode(val = preorder[0])
            preorder_left_new = preorder[1:(1+i)]
            inorder_left_new = inorder[0:i]
            left = self.buildTree(preorder_left_new,inorder_left_new)
            preorder_right_new = preorder[(1+i):len(preorder)] 
            inorder_right_new = inorder[(i+1):len(inorder)]
            right = self.buildTree(preorder_right_new,inorder_right_new)
            root.left = left
            root.right = right
            return root
# @lc code=end

