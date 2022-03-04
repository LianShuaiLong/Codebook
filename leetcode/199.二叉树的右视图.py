#
# @lc app=leetcode.cn id=199 lang=python3
#
# [199] 二叉树的右视图
#
# https://leetcode-cn.com/problems/binary-tree-right-side-view/description/
#
# algorithms
# Medium (65.44%)
# Likes:    631
# Dislikes: 0
# Total Accepted:    175K
# Total Submissions: 267.3K
# Testcase Example:  '[1,2,3,null,5,null,4]'
#
# 给定一个二叉树的 根节点 root，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。
# 
# 
# 
# 示例 1:
# 
# 
# 
# 
# 输入: [1,2,3,null,5,null,4]
# 输出: [1,3,4]
# 
# 
# 示例 2:
# 
# 
# 输入: [1,null,3]
# 输出: [1,3]
# 
# 
# 示例 3:
# 
# 
# 输入: []
# 输出: []
# 
# 
# 
# 
# 提示:
# 
# 
# 二叉树的节点个数的范围是 [0,100]
# -100  
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
    def rightSideView(self, root: TreeNode) -> List[int]:
        #层序遍历
        if not root:
            return []
        if not root.left and not root.right:
            return [root.val]
        layer_num = [[root.val]]
        layer_node = [[root]]
        while 1:
            cur_layer_num = []
            cur_layer_node = []
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
        return [item[-1] for item in layer_num]

# @lc code=end

