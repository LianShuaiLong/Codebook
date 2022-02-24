#
# @lc app=leetcode.cn id=237 lang=python3
#
# [237] 删除链表中的节点
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

#解题的重点在于找到node的前置结点
#方向一：通过构造环的方式找到前置结点->不可行
#方向二：通过交换结点值的方式找到前置结点
class Solution:
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        val_node = node.val
        tmp = node.next.val
        node.next.val = val_node
        node.val = tmp
        node.next = node.next.next
        
# @lc code=end

