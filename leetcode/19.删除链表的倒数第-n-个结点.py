#
# @lc app=leetcode.cn id=19 lang=python3
#
# [19] 删除链表的倒数第 N 个结点
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
                # initial
        # len = 0
        # cur = head
        # while cur:
        #     cur = cur.next
        #     len +=1
        # if n==len:
        #     return head.next
        # forward_step = len-n-1
        # t = head
        # while forward_step>0:
        #     t = t.next
        #     forward_step -=1
        # if t.next:
        #     t.next = t.next.next
        # return head
        # 进阶

        fast = head
        slow = head
        while n>0:
            if fast.next:
                fast = fast.next
                n -=1
            #已知题设条件n<=len(listnode),fast走的步数范围(0~(len(listnode)-1))
            #假如fast走到了tail,走的步数依然小于n,此时只有一种情况：n==len(listnode)
	        #此时就是删除头结点的情况,其余情况要么是删除中间结点要么是删除tail结点
	        #删除中间结点和删除tail结点均可以由下述步骤完成
            else:
                return head.next
        while fast and fast.next:
            fast = fast.next
            slow = slow.next
        if slow.next:
            slow.next = slow.next.next
        return head
# @lc code=end

