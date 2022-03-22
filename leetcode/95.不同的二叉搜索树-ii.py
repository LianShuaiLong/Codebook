#
# @lc app=leetcode.cn id=95 lang=python3
#
# [95] 不同的二叉搜索树 II
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import copy
class Solution:
    def changeVal(self,root:TreeNode,val):
        if not root:
            return None
        else:
            new_root = TreeNode(root.val)
            new_root.val = new_root.val+val
            new_root.left = self.changeVal(root.left,val)
            new_root.right = self.changeVal(root.right,val)
            return new_root
    def generateTrees(self, n: int) -> List[TreeNode]:
        if n==0:
            return []
        if n==1:
            node = TreeNode(n)
            return [node]
        dp = [[] for i in range(n+1)]
        dp[0] = [None]
        root = TreeNode(1)
        dp[1] = [root]
        root_1 = TreeNode(2)
        left_node = TreeNode(1)
        root_1.left = left_node
        root_2 = TreeNode(1)
        right_node = TreeNode(2)
        root_2.right = right_node
        dp[2] = [root_1,root_2]
        for i in range(3,n+1):
            #j当前root结点的取值
            for j in range(1,i+1):
                root_node = TreeNode(j)
                for left_root in dp[j-1]:
                    root_node.left = left_root
                    for right_root in dp[i-j]:
                        new_right_root = self.changeVal(right_root,j)
                        root_node.right = new_right_root
                        # 注意这里的深copy问题
                        # 后面的操作跟当前操作，拥有共同的基础操作，就要考虑deepcopy，例如回溯算法
                        dp[i].append(copy.deepcopy(root_node))
        return dp[-1]        
# @lc code=end

