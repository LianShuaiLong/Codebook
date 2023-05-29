#
# @lc app=leetcode.cn id=146 lang=python3
#
# [146] LRU 缓存
#

# @lc code=start
class biListNode:
    def __init__(self,key=None,value=None):
        self.prev = None
        self.next = None
        self.key = key
        self.value = value

class LRUCache:

    def __init__(self, capacity: int):
        self.capcity = capacity
        self.head = biListNode()
        self.tail = biListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        #dict里面应该存放的是结点
        self.hashmap = dict()
    def get(self, key: int) -> int:
        if key in self.hashmap:
            value = self.hashmap[key].value
            self.move_to_tail(self.hashmap[key])
            return value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.hashmap:
            self.hashmap[key].value = value
            self.move_to_tail(self.hashmap[key])
        else:
            if len(self.hashmap)==self.capcity:
                k = self.head.next.key
                del self.hashmap[k]
                #head和tail两个dummy结点,保证了这个操作的有效性
                self.head.next=self.head.next.next
                self.head.next.prev = self.head #注意这里是self.head.next.prev 不是self.head.next.next.prev
            new_node = biListNode(key,value)
            # self.hashmap[key] = new_node
            new_node.prev = self.tail.prev
            self.tail.prev.next = new_node
            self.tail.prev= new_node
            new_node.next = self.tail
            self.hashmap[key] = new_node #value是new_node的引用,赋值操作在进dict前后都可以
            
            
    def move_to_tail(self,node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.tail.prev.next = node
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev = node
        




# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
# @lc code=end

