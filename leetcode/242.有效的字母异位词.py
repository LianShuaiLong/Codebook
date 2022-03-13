#
# @lc app=leetcode.cn id=242 lang=python3
#
# [242] 有效的字母异位词
#

# @lc code=start
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_d = [0] * (ord('z')+1-ord('a'))
        for i in s:
            s_d[ord(i)-ord('a')]+=1
        for j in t:
            s_d[ord(j)-ord('a')]-=1
        res = set(s_d)
        return len(res)==1
# @lc code=end

