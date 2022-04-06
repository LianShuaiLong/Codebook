# 这种数据结构的dict与vallina dict不同之处：
#       O(1)时间复杂度以相同的概率返回'dict'里面的一个值
# 若直接对vallina dict的key进行list化，然后随机取，则时间复杂度为O(n)
# 空间换时间
from random import choice
class RandomDict:
    def __init__(self):
        self.hashmap = dict()#val:idx
        self.ram = list()
        self.valid_len = 0
    
    def remove(self,val):
        if val not in self.hashmap:
            return False
        else:
            idx = self.hashmap[val]
            self.hashmap[self.ram[self.valid_len-1]]=idx
            self.ram[idx],self.ram[self.valid_len-1] = self.ram[self.valid_len-1],self.ram[idx]
            self.valid_len-=1
            del self.hashmap[val]
            return True

    def insert(self,val):
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
    
    def get_random(self):
        return choice(self.ram[:self.valid_len])

    def get_total(self):
        return self.ram[:self.valid_len]

def test():
    operation_list = ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
    val_list = [[], [1], [2], [2], [], [1], [2], []]
    Obj = RandomDict()
    for k,v  in zip(operation_list,val_list):
        if k == 'RandomizedSet':
            print('null')
        elif k == 'insert':
            flag = Obj.insert(v[0])
            if not flag:
                print('False')
            else:
                print('True')
        elif k == 'remove':
            flag = Obj.remove(v[0])
            if not flag:
                print('False')
            else:
                print('True')
        elif k == 'getRandom':
            print(Obj.get_random())
        else:
            print(f'invalid operation:{k}')
            continue

if __name__=='__main__':
    test()

            
