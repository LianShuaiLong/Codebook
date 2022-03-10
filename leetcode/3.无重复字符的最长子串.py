#
# @lc app=leetcode.cn id=3 lang=python3
#
# [3] 无重复字符的最长子串
#

# @lc code=start
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        d_1={}#value:loc
        d_2={}#loc:value
        #添加有效子串index下限,防止超时
        valid_loc_begin = 0
        max_length = 0
        cur_length = 0
        for i in range(len(s)):
            if s[i] not in d_1:
                d_1[s[i]]=i
                d_2[i]=s[i]
            else:
                pre_loc = d_1[s[i]]
                #需要将上一个重复的字符之前的字符全部去掉
                for j in range(valid_loc_begin,pre_loc+1):
                    if j in d_2:
                        d_1.pop(d_2[j])
                        d_2.pop(j)
                        valid_loc_begin = max(valid_loc_begin,j)
                d_1[s[i]]=i
                d_2[i]=s[i]
            cur_length = len(d_1)
            max_length = max(max_length,cur_length)
        return max_length
# @lc code=end

