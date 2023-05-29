#
# @lc app=leetcode.cn id=23 lang=python3
#
# [23] 合并K个升序链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self,list1,list2):
        if not list1:
            return list2
        if not list2:
            return list1
        cur_list1 = list1
        cur_list2 = list2
        res = ListNode()
        cur_res = res
        while cur_list1 and cur_list2:
            val_list1 = cur_list1.val
            val_list2 = cur_list2.val
            if val_list1>val_list2:
                cur_res.next = cur_list2
                cur_list2 = cur_list2.next
            else:
                cur_res.next = cur_list1
                cur_list1 = cur_list1.next
            cur_res = cur_res.next
        if cur_list1:
            cur_res.next = cur_list1
        if cur_list2:
            cur_res.next = cur_list2
        return res.next
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # 按照顺序进行合并 
        # res = None
        # for i in range(len(lists)):
        #     res = self.mergeTwoLists(res,lists[i])
        # return res
        # 分治算法
        if len(lists)==0:
            return None
        elif len(lists)==1:
            return lists[0]
        elif len(lists)==2:
            return self.mergeTwoLists(lists[0],lists[1])
        else:
            return self.mergeTwoLists(self.mergeKLists(lists[:len(lists)//2]),self.mergeKLists(lists[len(lists)//2:len(lists)]))

# @lc code=end

