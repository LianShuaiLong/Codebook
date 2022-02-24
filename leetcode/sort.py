
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sort_method',type=str,default='0',help='0:guibing_sort,1:quick_sort')
args = parser.parse_args()

class ListNode:
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

def create_ListNode(data_list:list):
    head = ListNode()
    cur = head
    for data in data_list:
        new_node = ListNode(val=data)
        cur.next = new_node
        cur = cur.next
    return head.next

def print_ListNode(head:ListNode):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    print(res)

def guibing_sort(head:ListNode):
    if not head or not head.next:
        return head
    slow = head
    fast = head.next #保证链表可分，fast!=head,不然长度为2的时候会出错
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    mid = slow.next
    slow.next = None
    left = guibing_sort(head)
    right = guibing_sort(mid)
    new_node = ListNode()
    cur = new_node
    while left and right:
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

def quick_sort(head:ListNode):
    if not head or not head.next:return head
    big = None
    small = None
    equal = None
    val_benchmark = head.val
    cur = head
    while cur:
        tmp = cur
        cur = cur.next
        val_tmp = tmp.val
        if val_tmp>val_benchmark:
            tmp.next = big
            big = tmp
        elif val_tmp<val_benchmark:
            tmp.next = small
            small = tmp
        else:
            tmp.next = equal
            equal = tmp
    small = quick_sort(small)
    big = quick_sort(big)
    new_node = ListNode()
    cur_node = new_node
    while small:
        cur_node.next = small
        small = small.next
        cur_node = cur_node.next
    while equal:
        cur_node.next = equal
        equal = equal.next
        cur_node = cur_node.next
    while big:
        cur_node.next = big
        big = big.next
        cur_node = cur_node.next
    return new_node.next

if __name__=='__main__':
    input_list = [3,2,5,1,7,3]
    input_ListNode = create_ListNode(input_list)
    print('input ListNode:\n')
    print_ListNode(input_ListNode)
    sort_method = args.sort_method
    if sort_method == '0':
        print('=====归并排序=====')
        output_ListNode = guibing_sort(input_ListNode)
        print('guibing output ListNode:\n')
        print_ListNode(output_ListNode)
    elif sort_method == '1':
        print('=====快速排序=====')
        output_ListNode = quick_sort(input_ListNode)
        print('quick output ListNode:\n')
        print_ListNode(output_ListNode)
    else:
        raise ValueError('UNKNOWN SORT METHOD')
