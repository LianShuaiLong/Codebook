#
# @lc app=leetcode.cn id=102 lang=python3
#
# [102] 二叉树的层序遍历
#
# https://leetcode-cn.com/problems/binary-tree-level-order-traversal/description/
#
# algorithms
# Medium (64.43%)
# Likes:    1198
# Dislikes: 0
# Total Accepted:    491.8K
# Total Submissions: 763K
# Testcase Example:  '[3,9,20,null,null,15,7]'
#
# 给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。
# 
# 
# 
# 示例 1：
# 
# 
# 输入：root = [3,9,20,null,null,15,7]
# 输出：[[3],[9,20],[15,7]]
# 
# 
# 示例 2：
# 
# 
# 输入：root = [1]
# 输出：[[1]]
# 
# 
# 示例 3：
# 
# 
# 输入：root = []
# 输出：[]
# 
# 
# 
# 
# 提示：
# 
# 
# 树中节点数目在范围 [0, 2000] 内
# -1000 <= Node.val <= 1000
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
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        if not root.left and not root.right:
            return [[root.val]]
        layer_node = [[root]]
        layer_num = [[root.val]]
        while 1:
            cur_layer_node = []
            cur_layer_num = []
            for i in range(len(layer_node[-1])):
                node = layer_node[-1][i]
                if node.left:
                    cur_layer_node.append(node.left)
                    cur_layer_num.append(node.left.val)
                if node.right:
                    cur_layer_node.append(node.right)
                    cur_layer_num.append(node.right.val)
            if len(cur_layer_node)==0:
                break
            else:
                layer_node.append(cur_layer_node)
                layer_num.append(cur_layer_num)
        return layer_num

# @lc code=end

