#
# @lc app=leetcode.cn id=82 lang=python3
#
# [82] 删除排序链表中的重复元素 II
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
        dummy = ListNode()
        dummy_ = dummy
        cur = head
        cur_ = cur
        cnt = 0
        while cur_:
            val_cur = cur.val
            val_cur_ = cur_.val
            if val_cur_==val_cur:
                cnt+=1
                #注意这个判断，这个是针对tail结点的，当cur和cur_同时指向tail结点的时候，如果一味的
                #向后移动cur_结点,对于非重复值的tail结点丢失；所以需要先判断当前结点是否是非重复值的
                #tail结点,如果是的话,就将该结点添加到最终listnode上，并且移动cur_,保证跳出循环
                if not cur_.next:
                    if cnt == 1:
                        dummy_.next = cur
                        dummy_ = dummy_.next
                        dummy_.next = None
                cur_ = cur_.next       
            else:
                if cnt==1:
                    dummy_.next = cur
                    dummy_ = dummy_.next
                    dummy_.next = None
                cur = cur_
                cnt = 0
        return dummy.next 

# @lc code=end

