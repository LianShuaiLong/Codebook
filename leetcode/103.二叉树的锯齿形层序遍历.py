#
# @lc app=leetcode.cn id=103 lang=python3
#
# [103] 二叉树的锯齿形层序遍历
#
# https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/description/
#
# algorithms
# Medium (57.23%)
# Likes:    598
# Dislikes: 0
# Total Accepted:    207.6K
# Total Submissions: 362.7K
# Testcase Example:  '[3,9,20,null,null,15,7]'
#
# 给你二叉树的根节点 root ，返回其节点值的 锯齿形层序遍历 。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。
# 
# 
# 
# 示例 1：
# 
# 
# 输入：root = [3,9,20,null,null,15,7]
# 输出：[[3],[20,9],[15,7]]
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
# -100 <= Node.val <= 100
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
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        if not root.left and not root.right:
            return [[root.val]]
        stack_node_even = [root]
        stack_node_odd = []
        res = []
        cur_layer = 0
        while 1:
            if len(stack_node_even)>0 or len(stack_node_odd)>0:
                cur_layer_num = []
                if cur_layer%2==0: 
                    while len(stack_node_even)>0:
                        node = stack_node_even.pop()
                        cur_layer_num.append(node.val)
                        if node.left:
                            stack_node_odd.append(node.left)
                        if node.right:
                            stack_node_odd.append(node.right)
                else:
                    while len(stack_node_odd)>0:
                        node = stack_node_odd.pop()
                        cur_layer_num.append(node.val)
                        if node.right:
                            stack_node_even.append(node.right)
                        if node.left:
                            stack_node_even.append(node.left)
                cur_layer+=1
                res.append(cur_layer_num)
            else:
                break
        return res
# @lc code=end

