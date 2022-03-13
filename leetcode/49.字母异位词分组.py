#
# @lc app=leetcode.cn id=49 lang=python3
#
# [49] 字母异位词分组
#

# @lc code=start
from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]: 
        length = ord('z')+1-ord('a')
        res_dict=defaultdict(list)
        res = []
        for idx,item in enumerate(strs):
            new_key = [0]*length
            for i in item:
                loc = ord(i)-ord('a')
                new_key[loc]+=1 
            #需要用字符拼接' '，防止10的情况 
            n_k = ' '.join([str(item) for item in new_key])
            res_dict[n_k].append(idx)
        for k,v in res_dict.items():
            r = [strs[i] for i in v]
            res.append(r) 
        return res

# @lc code=end

