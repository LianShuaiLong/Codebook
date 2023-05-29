#
# @lc app=leetcode.cn id=8 lang=python3
#
# [8] 字符串转换整数 (atoi)
#

# @lc code=start
class Solution:
    def myAtoi(self, s: str) -> int:
        i = 0
        while s[i]==' ':
            i+=1
        res_mul = 0
        #res_div = 0
        pos_or_neg = True
        #mul_or_div = True
        #div_ = 0
        for j in range(i,len(s)):
            if (s[j]>='a' and s[j]<='z') or (s[j]>='A' and s[j]<='Z') or s[j]==' ' or s[j]=='.':
                if pos_or_neg:
                    return res_mul#+res_div/pow(10,div_)
                else:
                    return -(res_mul)#+res_div/pow(10,div_))
            else:
                if s[j]=='-':
                    pos_or_neg = False
                # elif s[j]=='.':
                #     mul_or_div = False
                else:
                    res_mul = res_mul*10+s_int
                    # s_int = int(s[j])
                    # if mul_or_div:
                    #     res_mul = res_mul*10+s_int
                    # else:
                    #     div_+=1
                    #     res_div = res_div*10+s_int 
        if pos_or_neg:
            return res_mul+res_div/pow(10,div_)
        else:
            return -(res_mul+res_div/pow(10,div_))

# @lc code=end

