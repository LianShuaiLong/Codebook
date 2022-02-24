#
# @lc app=leetcode.cn id=83 lang=python3
#
# [83] 删除排序链表中的重复元素
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        if not head or not head.next:
            return head
        fast = head
        slow = head
        while fast:
            val_slow = slow.val
            val_fast = fast.val
            if val_fast == val_slow:
                fast = fast.next
            else:
                slow.next = fast
                slow = slow.next
        slow.next = fast
        return head
            
# @lc code=end

