#
# @lc app=leetcode.cn id=108 lang=python3
#
# [108] 将有序数组转换为二叉搜索树
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if len(nums)==0:
            return None
        elif len(nums)==1:
            node = TreeNode(val=nums[0])
            return node
        else:   
            # 分不分都行,只是对于偶数节点数是left-root还是root-right的区别
            # if len(nums)%2==0:
            #     mid = len(nums)//2-1
            #     root = TreeNode(val=nums[mid])
            #     left = self.sortedArrayToBST(nums[0:mid])
            #     right = self.sortedArrayToBST(nums[(mid+1):len(nums)])
            #     root.left = left
            #     root.right = right
            #     return root
            # else:
            mid = len(nums)//2
            root = TreeNode(val = nums[mid])
            left = self.sortedArrayToBST(nums[0:mid])
            right = self.sortedArrayToBST(nums[(mid+1):len(nums)])
            root.left = left
            root.right = right
            return root
            
                

# @lc code=end

