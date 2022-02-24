#
# @lc app=leetcode.cn id=86 lang=python3
#
# [86] 分隔链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: ListNode, x: int) -> ListNode:
        h_s = ListNode()
        h_s_ = h_s
        h_l = ListNode()
        h_l_ = h_l
        cur = head
        if not cur or not cur.next:
            return cur
        while cur:
            cur_val = cur.val
            tmp = cur.next
            if cur_val< x:
                h_s.next = cur
                h_s = h_s.next
                h_s.next = None
            else:
                h_l.next = cur
                h_l = h_l.next
                h_l.next = None
            cur = tmp
        h_s.next = h_l_.next
        return h_s_.next

                
# @lc code=end

