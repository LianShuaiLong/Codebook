#
# @lc app=leetcode.cn id=91 lang=python3
#
# [91] 解码方法
#

# @lc code=start
class Solution:
    def numDecodings(self, s: str) -> int:
        #数字范围时1-26
        dp = [1 for i in range(2*len(s))]
        if s[0]=='0':
            return 0
        for i in range(1,len(s)):
            # 需要分的情况
            # 当前时0:
            #        前面是[1,2] dp[i-2]
            #        前面是其它，X0不能解码X=0,[3,9]
            # 当前不是0:
            #        当前是[1,6]:
            #            前面是[1,2] dp[i-1]+dp[i-2]
            #            前面是其它：dp[i-1]
            #        当前是[7,9]:
            #            前面是1，dp[i-1]+dp[i-2]
            #            前面是其它：dp[i-1]
            if s[i]=='0':
                if s[i-1]>='1' and s[i-1]<='2':
                    dp[i]=dp[i-2]
                else:
                    return 0
            elif s[i]>='1' and s[i]<='6':
                if s[i-1]>='1' and s[i-1]<='2':
                    dp[i] = dp[i-1]+dp[i-2]
                else:
                    dp[i]=dp[i-1]
            else:
                if s[i-1]=='1':
                    dp[i] = dp[i-1]+dp[i-2]
                else:
                    dp[i]=dp[i-1]
        return dp[len(s)-1]
# @lc code=end

