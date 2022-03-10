#
# @lc app=leetcode.cn id=113 lang=python3
#
# [113] 路径总和 II
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:

    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        path = []
        res = []

        def dfs(root,targetSum):
            if not root:
                return
            path.append(root.val)
            targetSum-=root.val
            if not root.left and not root.right and targetSum==0:
                #path[:]深复制，得到path的一个副本-传递拷贝
                #如果直接append(path)的话，后续path操作会影响到res-传递引用
                res.append(path[:])
            dfs(root.left,targetSum)
            dfs(root.right,targetSum)
            #注意这里的pop操作
            path.pop()
        dfs(root,targetSum)
        return res    
            
# @lc code=end

