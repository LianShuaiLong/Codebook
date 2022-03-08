#
# @lc app=leetcode.cn id=109 lang=python3
#
# [109] 有序链表转换二叉搜索树
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        # 相比于将有序数组转换为平衡二叉树,将有序链表转为平衡二叉树,需要利用快慢指针分割有序链表
        if not head:
            return None
        elif not head.next:
            root = TreeNode(val=head.val)
            return root
        else:
            dummy = ListNode()
            dummy.next = head
            fast = dummy
            slow = dummy
            new_p = dummy
            while fast and fast.next:
                fast = fast.next.next
                slow = slow.next
            root = TreeNode(val=slow.val)
            right = self.sortedListToBST(slow.next)
            slow.next = None
            while new_p.next!=slow:
                new_p = new_p.next
            new_p.next = None
            # 注意这里()参数不是head,因为left可能是空
            # 如果设置为head,就错误的保证了left至少有一个结点
            left = self.sortedListToBST(dummy.next)
            root.left = left
            root.right = right
            return root
# @lc code=end

