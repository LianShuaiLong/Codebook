# LRU这种数据结构在推荐系统中可以用来存储embedding(user,item,...)
# 例如将embedding存在参数服务器中，假设存在redis里面(Redis的全称是remote dictionary server(远程字典服务器)，它以字典结构存储数据(key-value))
# O(1)的时间复杂度取embedding -----模型训练,serving......
# O(1)的时间复杂度去除embedding -----item不再投放，user注销账号......
# O(1)的时间复杂度新增embedding-----new user,new item......
# 当embedding的存储空间满了之后，O(1)的时间复杂度去除最长时间不用的embedding
class biListNode:#O(1)的时间复杂度将数据A从中间移到末尾，并将数据A后边的数据前移一位
    def __init__(self,key=None,value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
class LRU:
    def __init__(self,capcity):
        self.capcity = capcity #申请的redis空间大小
        self.hashmap = dict()
        self.head = biListNode()
        self.tail = biListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        
    #新增item embedding,user embedding
    def put(self,key,value):
        if key in self.hashmap:
            self.hashmap[key].value = value
            self.move_to_tail(self.hashmap[key])
        else:
            # 如果当前存储空间已满，则先删除最久不用的(k,v)(biListNode的第一个有效结点)
            if len(self.hashmap)==self.capcity:
                k = self.head.next.key
                del self.hashmap[k]
                self.head.next = self.head.next.next
                self.head.next.prev = self.head
            new_node = biListNode(key=key,value=value)
            self.tail.prev.next = new_node
            new_node.prev = self.tail.prev
            new_node.next = self.tail
            self.tail.prev = new_node
            self.hashmap[key] = new_node
    def get(self,key):
        if key in self.hashmap:
            node = self.hashmap[key]
            self.move_to_tail(node)
            return node.value
        else:
            return -1

    def move_to_tail(self,node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.tail.prev.next = node
        node.prev = self.tail.prev
        self.tail.prev = node
        node.next = self.tail

    def print_lru(self):
        for k,v in self.hashmap.items():
            print(f'{k}:{v.value}')