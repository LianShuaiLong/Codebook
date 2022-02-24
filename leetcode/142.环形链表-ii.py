#
# @lc app=leetcode.cn id=142 lang=python3
#
# [142] 环形链表 II
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        fast_pointer = head
        slow_pointer = head
        if not head or not head.next:
            return None
        while fast_pointer and fast_pointer.next:
            fast_pointer = fast_pointer.next.next
            slow_pointer = slow_pointer.next
            if slow_pointer == fast_pointer:
                slow_pointer = head
                while slow_pointer!= fast_pointer:
                    slow_pointer = slow_pointer.next
                    fast_pointer = fast_pointer.next
                return slow_pointer
        return None
           
        
# @lc code=end

