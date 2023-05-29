#
# @lc app=leetcode.cn id=56 lang=python3
#
# [56] 合并区间
#

# @lc code=start
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals = sorted(intervals,key=lambda k: k[0])
        left_list = []
        right_list = []
        n = len(intervals)
        if n==0:
            return intervals
        else:
            tmp = [intervals[0][0],intervals[0][1]]
            for i in range(1,n):
                l = intervals[i][0]
                r = intervals[i][1]
                if l<=tmp[1]:
                    if r<=tmp[1]:
                        continue
                    else:
                        tmp[1] = r
                else:
                    left_list.append(tmp[0])
                    right_list.append(tmp[1])
                    tmp[0] = intervals[i][0]
                    tmp[1] = intervals[i][1]
            left_list.append(tmp[0])
            right_list.append(tmp[1])
            res = []
            for left,right in zip(left_list,right_list):
                res.append([left,right])
            return res
                
# @lc code=end

