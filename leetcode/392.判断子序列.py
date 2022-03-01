#
# @lc app=leetcode.cn id=392 lang=python3
#
# [392] 判断子序列
#

# @lc code=start
# 先排序后二分 ×
# 双指针 √
# 整体思路:i指针在s上进行操作，j指针在t上操作
# 如果当前s[i]与t[j]相同，则下一步在[j+1:len(t)]
# 范围判断是否存在s[i+1],直至判断s[len(s)-1]也在
# [j`,len(t)]范围内，则证明s是t的子序列；若在判断
#
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        s_len = len(s)
        t_len = len(t)
        i = 0
        j = 0
        while i<s_len and j<t_len:
            s_cur = s[i]
            if t[j] == s_cur:
                i+=1
            # 注意这里,无论当前t[j]与s_cur是否相等,都应该有j+=1
            # 操作,否则如果遇到s_cur后面全是与s_cur相等的元素,
            # 就会误判
            j+=1
        return i==s_len
        
# @lc code=end

