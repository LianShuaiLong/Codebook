#
# @lc app=leetcode.cn id=101 lang=python3
#
# [101] 对称二叉树
#
# https://leetcode-cn.com/problems/symmetric-tree/description/
#
# algorithms
# Easy (57.13%)
# Likes:    1767
# Dislikes: 0
# Total Accepted:    509.3K
# Total Submissions: 890.9K
# Testcase Example:  '[1,2,2,3,4,4,3]'
#
# 给你一个二叉树的根节点 root ， 检查它是否轴对称。
# 
# 
# 
# 示例 1：
# 
# 
# 输入：root = [1,2,2,3,4,4,3]
# 输出：true
# 
# 
# 示例 2：
# 
# 
# 输入：root = [1,2,2,null,3,null,3]
# 输出：false
# 
# 
# 
# 
# 提示：
# 
# 
# 树中节点数目在范围 [1, 1000] 内
# -100 <= Node.val <= 100
# 
# 
# 
# 
# 进阶：你可以运用递归和迭代两种方法解决这个问题吗？
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
    # 递归方法
    # def isSame(self,root1:TreeNode,root2:TreeNode)->bool:
    #     if root1 and root2:
    #         if root1.val!=root2.val:
    #             return False
    #         else:
    #             return self.isSame(root1.left,root2.right) and self.isSame(root1.right,root2.left)
    #     elif not root1 and not root2:
    #         return True
    #     else:
    #         return False
            
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return False
        # 递归方法
        # return self.isSame(root.left,root.right) 
        # 循环方法(BFS)
        else:
            layer = []
            layer.append([root])
            while 1:
                cur_layer=[]
                for i in range(len(layer[-1])):
                    node = layer[-1][i]
                    node_duichen = layer[-1][len(layer[-1])-1-i]
                    if node.left and node_duichen.right:
                        if node.left.val == node_duichen.right.val:
                            cur_layer.append(node.left)
                        else:
                            return False
                    elif not node.left and not node_duichen.right:
                        pass #这里不是continue
                    else:
                        return False
                    if node.right and node_duichen.left:
                        if node.right.val == node_duichen.left.val:
                            cur_layer.append(node.right)
                        else:
                            return False
                    elif not node.right and not node_duichen.left:
                        pass #这里不是continue
                    else:
                        return False
                if len(cur_layer)>0 and len(cur_layer)%2!=0:
                    return False
                elif len(cur_layer)>0 and len(cur_layer)%2==0:
                    layer.append(cur_layer)
                else:
                    break
            return True
     
# @lc code=end

