#
# @lc app=leetcode.cn id=110 lang=python3
#
# [110] 平衡二叉树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        # Top to Down
        # def Height(root):
        #     if not root:
        #         return 0
        #     elif not root.left and not root.right:
        #         return 1
        #     else:
        #         return 1+max(Height(root.left),Height(root.right))
        # if not root:
        #     return True
        # return abs(Height(root.left)-Height(root.right))<=1 and self.isBalanced(root.left) and self.isBalanced(root.right)
        # Down to Top
        # 判断一棵树是否是平衡二叉树，先判断左右子树是否是平衡二叉树
        # 若是则返回其正确高度，否则返回-1，最后判断root结点的高度是否大于0
        def height(root):
            if not root:
                return 0
            else:
                h_left = height(root.left)
                h_right = height(root.right)
                # 注意这里需要先判断两个子树各自是否是平衡二叉树
                # 如果两者都是平衡二叉树，再判断两个子树的高度差
                if h_left == -1 or h_right ==-1 or abs(h_left-h_right)>1:
                    return -1
                else:
                    return 1+max(h_left,h_right)
        return height(root)>=0

# @lc code=end

