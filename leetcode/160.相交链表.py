#
# @lc app=leetcode.cn id=160 lang=python3
#
# [160] 相交链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        cur_A = headA
        cur_B = headB
        len_A = 0
        len_B = 0
        if not cur_A or not cur_B:
            return None
        while cur_A:
            len_A+=1
            cur_A = cur_A.next
        while cur_B:
            len_B+=1
            cur_B = cur_B.next
        cur_A = headA
        cur_B = headB
        dif_AB = len_A-len_B
        if dif_AB==0:
            while cur_A!=cur_B:
                cur_A = cur_A.next
                cur_B = cur_B.next
            return cur_A
        elif dif_AB>0:
            while dif_AB>0:
                cur_A = cur_A.next
                dif_AB -=1
            while cur_A!=cur_B:
                cur_A = cur_A.next
                cur_B = cur_B.next
            return cur_A
        else:
            while dif_AB<0:
                cur_B = cur_B.next
                dif_AB+=1
            while cur_A!=cur_B:
                cur_A = cur_A.next
                cur_B = cur_B.next
            return cur_A
        
# @lc code=end

