#
# @lc app=leetcode.cn id=100 lang=python3
#
# [100] 相同的树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        # recurrent
        # if not p and not q:
        #     return True
        # elif not p or not q:
        #     return False
        # else:
        #     if p.val != q.val:
        #         return False
        #     else:
        #         return self.isSameTree(p.left,q.left) and self.isSameTree(p.right,q.right)
        # BFS
        if not p and not q:
            return True
        elif not p or not q:
            return False
        else:
            if p.val!=q.val:
                return False
            else:
                p_list = [[p]]
                q_list = [[q]]
                while 1:
                    p_cur_layer = []
                    q_cur_layer = []
                    for p_node,q_node in zip(p_list[-1],q_list[-1]):
                        p_node_val = p_node.val
                        q_node_val = q_node.val
                        if p_node_val!=q_node_val:
                            return False
                        else:
                            if p_node.left and q_node.left:
                                p_cur_layer.append(p_node.left)
                                q_cur_layer.append(q_node.left)
                            elif not p_node.left and not q_node.left:
                                pass
                            else:
                                return False
                            if p_node.right and q_node.right:
                                p_cur_layer.append(p_node.right)
                                q_cur_layer.append(q_node.right)
                            elif not p_node.right and not q_node.right:
                                pass
                            else:
                                return False
                    if len(p_cur_layer)==0:
                        return True
                    p_list.append(p_cur_layer)
                    q_list.append(q_cur_layer)
                

# @lc code=end

