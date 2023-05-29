#
# @lc app=leetcode.cn id=57 lang=python3
#
# [57] 插入区间
#

# @lc code=start
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # 重点是找到newInterval所在的位置
        # 可能在intervals[-1]的位置,注意这个
        # 可能是在intervals[i]的位置,其中i>=0
        n = len(intervals)
        if n==0:
            return [newInterval]
        new_left = newInterval[0]
        new_right = newInterval[1]
        if new_left>=intervals[0][0]:
            idx = 1
            while idx<n:
                if intervals[idx-1][0]<=new_left and intervals[idx][0]>=new_left:
                    break
                idx+=1
            location = idx
            left_list = []
            right_list = []
            #就在location-1之后开始考虑合并区间
            idx = 0
            while idx<location-1:
                left_list.append(intervals[idx][0])
                right_list.append(intervals[idx][1])
                idx+=1
            tmp = [intervals[location-1][0],intervals[location-1][1]]
            if new_left<=tmp[1]:
                if new_right>tmp[1]:
                    tmp[1] = new_right
            else:
                left_list.append(tmp[0])
                right_list.append(tmp[1])
                tmp[0] = new_left
                tmp[1] = new_right
            for i in range(location,n):
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
        else:
            left_list = []
            right_list = []
            tmp = [new_left,new_right]
            for i in range(n):
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

