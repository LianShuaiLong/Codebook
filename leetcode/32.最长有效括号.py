#
# @lc app=leetcode.cn id=32 lang=python3
#
# [32] 最长有效括号
#

# @lc code=start
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        # 只适合"()()()"的情况
        # 不适合"(())"的情况
        # valid_brackets=[]
        # max_valid_bracket = 0
        # for c in s:
        #     if c =='(':
        #         if len(valid_brackets)==0 or valid_brackets[-1]==')':
        #             valid_brackets.append(c)
        #         else:
        #             while len(valid_brackets)>0:
        #                 valid_brackets.pop()
        #             valid_brackets.append(c)
        #     else:
        #         if len(valid_brackets)==0:
        #             continue
        #         else:
        #             if valid_brackets[-1]=='(':
        #                 valid_brackets.append(c)
        #                 cur_valid_bracket = len(valid_brackets)
        #                 max_valid_bracket = max(max_valid_bracket,cur_valid_bracket)
        #             else:
        #                 while len(valid_brackets)>0:
        #                     valid_brackets.pop()
        # return max_valid_bracket
        # dp[i]代表以s[i]结尾最长有效子串长度,以2为单位进行状态转移
        # 当s[i]=='(',则dp[i]=0
        # 当s[i]==')',
        # 若s[i-1]=='(',即...()的形式,则dp[i]=dp[i-2]+2
        # 若s[i-1]==')',即...))的形式,则dp[i] = dp[i-1]+dp[i-dp[i-1]-2]+2
        # 若s[i]是包含前面有效子串的大子串的一部分，那么一定有与之对应的'('
        # 此时dp[i]=dp[i-1]+2+dp[i-dp[i-1]-2],后者'('之前的有效子串长度
        # 若不是,则dp[i]=0
        max_valid_bracket = 0
        #设置这个长度防止dp[i-dp[i-1]-2]循环回来导致死循环,尤其s[-1]时候"(())",求解dp[-1]的时候,dp[i-dp[i-1]-2]=dp[-1]
        dp = [0 for i in range(2*len(s))]
        for i in range(len(s)):
            if s[i]=='(':
                dp[i]=0
            else:
                if i == 0:
                    continue
                elif i==1:
                    dp[i] = 2 if s[0]=='(' else 0
                else:
                    if s[i-1]=='(':
                        dp[i] = dp[i-2]+2
                    else:
                        #前置条件防止与s[-1]进行匹配
                        if i-dp[i-1]-1>=0 and s[i-dp[i-1]-1]=='(':
                            dp[i] = dp[i-1]+2+dp[i-dp[i-1]-2]
                        else:
                            dp[i] = 0
                max_valid_bracket = max(max_valid_bracket,dp[i])
        return max_valid_bracket

# @lc code=end

