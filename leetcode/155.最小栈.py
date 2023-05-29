#
# @lc app=leetcode.cn id=155 lang=python3
#
# [155] 最小栈
#

# @lc code=start
class MinStack:

    def __init__(self):
        self.ordinary_list = []
        self.min_list = [float('inf')]
        

    def push(self, val: int) -> None:
        self.ordinary_list.append(val)
        self.min_list.append(min(self.min_list[-1],val))
        

    def pop(self) -> None:
        self.ordinary_list.pop()
        self.min_list.pop()
        

    def top(self) -> int:
        return self.ordinary_list[-1]

    def getMin(self) -> int:
        return self.min_list[-1]



# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
# @lc code=end

