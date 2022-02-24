#
# @lc app=leetcode.cn id=206 lang=python3
#
# [206] 反转链表
#

# @lc code=start
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        new_node = ListNode()
        cur = head
        if not cur:
            return None
        if not cur.next:
            return cur
        while cur:
            tmp = cur.next
            cur.next = new_node.next
            new_node.next = cur
            cur = tmp
            # 错误写法(没有保存链表剩余数据)
            # c_node= head
            # c_node.next = new_node.next
            # new_node.next = c_node
            # head = head.next
        return new_node.next
# @lc code=end

