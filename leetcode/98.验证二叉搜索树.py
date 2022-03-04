#
# @lc app=leetcode.cn id=98 lang=python3
#
# [98] 验证二叉搜索树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        res = []
        if not root:
            return False
        if not root.left and not root.right:
            return True
        #思路:对二叉树进行中序遍历，看结果是都是一个升序数组
        res = self.mid_view(root)
        for i in range(1,len(res)):
            if res[i]<=res[i-1]:
                return False
        return True
    def mid_view(self,root:TreeNode) ->List[int]:
        if not root:
            return []
        if not root.left and not root.right:
            return [root.val]
        res = []
        if root.left:
            node_left = self.mid_view(root.left)
            res.extend(node_left)
        res.append(root.val)
        if root.right:
            node_right = self.mid_view(root.right)
            res.extend(node_right)
        return res
# @lc code=end

