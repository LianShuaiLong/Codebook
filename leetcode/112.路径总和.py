#
# @lc app=leetcode.cn id=112 lang=python3
#
# [112] 路径总和
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def dfs(self,root,targetSum):
        # 注意返回值
        if not root:
            return -1001
        else:
            # 注意这里要是叶子结点才能返回0
            if root.val == targetSum and not root.left and not root.right:
                return 0
            else:
                if self.dfs(root.left,targetSum-root.val)==0:
                    return 0
                elif self.dfs(root.right,targetSum-root.val)==0:
                    return 0
                # 注意这里的返回值,不能返回targeSum/targetSum-roo.val
                # 因为存在targetSum本身取值为0的情况，而最终我们要根据返回值
                # 是否为0判断是否存在对应的路径
                # 如：targetSum = 0,root.val = 0,left=1,right=2 
                else:
                    return -1001

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        else:
            return self.dfs(root,targetSum)==0
# @lc code=end

