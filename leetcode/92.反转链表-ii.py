#
# @lc app=leetcode.cn id=92 lang=python3
#
# [92] 反转链表 II
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
#注意提示，只要求了left>=1，所以将cur初始化为head,然后向后移动left-1-1次，使其到达第(left-1)个结点
#并不可靠；将cur初始化为cur=dummy & dummy.next = head,然后将cur向后移动left-1次到达第(left-1)个
#结点比较合理；
class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        if not head.next:return head
        if left==right:return head

        step_left = left-1
        dummy = ListNode()
        dummy.next = head
        cur = dummy
        for i in range(step_left):
            cur = cur.next
        d = cur
        dummy_1 = cur.next
        cur.next = None
        cur = dummy_1
        for i in range(right-left):
            cur = cur.next
        dummy_2 = cur.next
        cur.next = None

        while dummy_1:
            tmp = dummy_1.next
            dummy_1.next = dummy_2
            dummy_2 = dummy_1
            dummy_1 = tmp
        d.next = dummy_2
        return dummy.next

# @lc code=end

