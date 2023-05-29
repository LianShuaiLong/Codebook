#
# @lc app=leetcode.cn id=380 lang=python3
#
# [380] O(1) 时间插入、删除和获取随机元素
#

# @lc code=start
from random import choice
class RandomizedSet:
    # self.ram用于存放val
    # self.hashmap用于存放val:idx
    def __init__(self):
        self.hashmap = dict()
        self.valid_len = 0
        self.ram = list()

    # 对于self.hashmap,新插入的数据val:self.val_len
    # 对于self.ram,新插入的数据：
    #    若当前已经有删除的数据，则一定是self.val_len<len(self.ram),此时self.ram[self.val_len]=val即可
    #    若当前没有删除的数据，则self.val_len==len(self.ram),此时self.ram.append(val)
    #在上述操作之后！！！进行self.val_len+1操作
    def insert(self, val: int) -> bool:
        if val in self.hashmap:
            return False
        else:
            self.hashmap[val]=self.valid_len
            if self.valid_len<len(self.ram):
                self.ram[self.valid_len]=val
            else:
                self.ram.append(val)
            self.valid_len+=1
            return True

    # val在self.hashmap,先获取其对应的idx,然后对self.ram的idx位置与self.valid_len位置进行交换
    # 并进行self.val_len-1操作，最后在self.hashmap中删除val
    def remove(self, val: int) -> bool:
        if val in self.hashmap:
            idx_val = self.hashmap[val]
            self.hashmap[self.ram[self.valid_len-1]]=idx_val
            self.ram[idx_val],self.ram[self.valid_len-1]=self.ram[self.valid_len-1],self.ram[idx_val]
            self.valid_len-=1
            del self.hashmap[val]
            return True
        else:
            return False

    def getRandom(self) -> int:
        return choice(self.ram[:self.valid_len])



# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
# @lc code=end

