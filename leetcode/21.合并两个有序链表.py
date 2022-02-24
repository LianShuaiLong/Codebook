#
# @lc app=leetcode.cn id=21 lang=python3
#
# [21] 合并两个有序链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur_list1 = list1
        cur_list2 = list2
        if not list1:
            return list2
        if not list2:
            return list1
        res = ListNode()
        cur_res = res
        while cur_list1 and cur_list2:
            val_list1 = cur_list1.val
            val_list2 = cur_list2.val
            if val_list1<val_list2:
                cur_res.next = cur_list1
                cur_list1 = cur_list1.next
            else:
                cur_res.next = cur_list2
                cur_list2 =cur_list2.next
            cur_res = cur_res.next
        if cur_list1:
            cur_res.next = cur_list1
        if cur_list2:
            cur_res.next = cur_list2
        return res.next
# @lc code=end

