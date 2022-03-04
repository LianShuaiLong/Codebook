#
# @lc app=leetcode.cn id=99 lang=python3
#
# [99] 恢复二叉搜索树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorder(self,root):
        if not root:
            return []
        if not root.left and not root.right:
            return [root]
        res = []
        if root.left:
            node_left = self.inorder(root.left)
            res.extend(node_left)
        res.append(root)
        if root.right:
            node_right = self.inorder(root.right)
            res.extend(node_right)
        return res
        
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        node_list = self.inorder(root)
        if len(node_list)==0:
            return 
        elif len(node_list)==1:
            return
        else:
            cnt = 0
            node_1_idx = -1
            node_2_idx = -1
            # print([node.val for node in node_list])
            for i in range(1,len(node_list)):
                if node_list[i].val<=node_list[i-1].val:
                    if cnt==0:
                        node_1_idx = i-1
                        #注意这里的node_2_idx
                        #遇到第一对逆序的时候需要将node_2_idx先赋值
                        #如果还有第二对的逆序(最多两对)，则将node_2_idx重新赋值
                        node_2_idx = i
                        cnt+=1
                    else:
                        node_2_idx = i
                        cnt=0
            tmp = node_list[node_1_idx].val
            node_list[node_1_idx].val = node_list[node_2_idx].val
            node_list[node_2_idx].val = tmp
            return


        

# @lc code=end

