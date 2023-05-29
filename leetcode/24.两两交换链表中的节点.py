#
# @lc app=leetcode.cn id=24 lang=python3
#
# [24] 两两交换链表中的节点
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        dummy = ListNode()
        d_dummy = dummy
        dummy.next = head
        slow,fast = dummy,dummy
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast:
                tmp = fast.next
                dummy.next = fast
                fast.next = slow
                slow.next = tmp
                fast = slow
                dummy = slow
            else:
                return d_dummy.next
        return d_dummy.next
            
# @lc code=end

