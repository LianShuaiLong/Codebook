#
# @lc app=leetcode.cn id=148 lang=python3
#
# [148] 排序链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:

    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        # 快慢指针拆分链表,子链表排序,然后合并两个有序链表
        slow = head
        fast = head.next#注意这里,fast不能等于head,否则长度为2的时候，会导致不可分，注意与环形链表的不同
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next
        slow.next = None
        left = self.sortList(head)
        right = self.sortList(mid)
        # 合并两个有序链表
        new_node = ListNode()
        cur = new_node
        while left and right:
            val_left = left.val
            val_right = right.val
            if left.val<right.val:
                cur.next = left
                left = left.next
                cur = cur.next
                cur.next = None
            else:
                cur.next = right
                right = right.next
                cur = cur.next
                cur.next = None
        if left:
            cur.next = left
        if right:
            cur.next = right
        return new_node.next
        # 快速排序
        # big = None
        # small = None
        # same = None
        # cur = head
        # val_benchmark = head.val
        # while cur:
        #     tmp = cur
        #     cur = cur.next
        #     val_tmp = tmp.val
        #     if val_tmp < val_benchmark:
        #         tmp.next =  small
        #         small = tmp
        #     elif val_tmp > val_benchmark:
        #         tmp.next = big
        #         big = tmp
        #     else:
        #         tmp.next = same
        #         same = tmp
        # big_nodes = self.sortList(big)
        # small_nodes = self.sortList(small)
        # new_node = ListNode()
        # cur_node = new_node
        # #按顺序拼接
        # while small_nodes:
        #   cur_node.next = small_nodes
        #   small_nodes = small_nodes.next
        #   cur_node = cur_node.next
        # while same:
        #   cur_node.next = same
        #   same = same.next
        #   cur_node = cur_node.next
        # while big_nodes:
        #   cur_node.next = big_nodes
        #   big_nodes = big_nodes.next
        #   cur_node = cur_node.next
        # return new_node.next
         
                
# @lc code=end

