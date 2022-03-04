#
# @lc app=leetcode.cn id=5 lang=python3
#
# [5] 最长回文子串
#
# https://leetcode-cn.com/problems/longest-palindromic-substring/description/
#
# algorithms
# Medium (36.24%)
# Likes:    4765
# Dislikes: 0
# Total Accepted:    896.9K
# Total Submissions: 2.5M
# Testcase Example:  '"babad"'
#
# 给你一个字符串 s，找到 s 中最长的回文子串。
# 
# 
# 
# 示例 1：
# 
# 
# 输入：s = "babad"
# 输出："bab"
# 解释："aba" 同样是符合题意的答案。
# 
# 
# 示例 2：
# 
# 
# 输入：s = "cbbd"
# 输出："bb"
# 
# 
# 
# 
# 提示：
# 
# 
# 1 <= s.length <= 1000
# s 仅由数字和英文字母组成
# 
# 
#

# @lc code=start
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # 回文的特点:正向和逆向完全相同
        # 思路:将原字符串反过来形成新的字符串s_reverse,然后求两者最长公共子串
        # s_reverse=[]
        # for i in range(len(s)-1,-1,-1):
        #     s_reverse.append(s[i])
        # s_r = ''.join(s_reverse)
        # s_matrix = [[0 for i in range(len(s))] for j in range(len(s))]
        # max_palindrome_len = 0
        # max_palindrome = ''
        # #边界也是要考虑的
        # for i in range(len(s)):
        #     if s_r[0] == s[i]:
        #         s_matrix[0][i]=1
        #     else:
        #         s_matrix[0][i]=0
        #     if s_matrix[0][i]>max_palindrome_len:
        #         max_palindrome_len = s_matrix[0][i]
        #         max_palindrome = s[(i+1-max_palindrome_len):(i+1)]    
        # for i in range(len(s)):
        #     if s_r[i] == s[0]:
        #         s_matrix[i][0]=1
        #     else:
        #         s_matrix[i][0]=0
        #     if s_matrix[i][0]>max_palindrome_len:
        #         max_palindrome_len = s_matrix[i][0]
        #         max_palindrome = s[(i+1-max_palindrome_len):(i+1)]    
        # for i in range(1,len(s)):
        #     for j in range(1,len(s)):
        #         if s_r[i]==s[j]:
        #             #需要判断一下是否是回文串,防止abc435cba的情况
        #             before_rev = len(s)-1-i+s_matrix[i-1][j-1]
        #             if j != before_rev:
        #                 s_matrix[i][j]=0
        #             else:
        #                 #当前对比相等后，需要两个字符串在前一位基础上写状态转移方程，所以是对角线
        #                 s_matrix[i][j]=s_matrix[i-1][j-1]+1
        #                 if s_matrix[i][j]>max_palindrome_len:
        #                     max_palindrome_len = s_matrix[i][j] 
        #                     max_palindrome = s[(i+1-max_palindrome_len):(i+1)]    
        #         else:
        #             s_matrix[i][j]=0
        # return max_palindrome
        #思路二：动态规划[i,j]是回文，则[i+1,j-1]肯定也是回文子串
        m = len(s)
        if m==1:
            return s
        if m==2:
            if s[0] == s[1]:
                return s
            else:
                return s[0]
        max_len = 1
        max_s = s[0]
        matrix = [[False for i in range(m)] for i in range(m)]
        for i in range(m):
            matrix[i][i] = True #s[i:(j+1)]是否是回文子串
        #固定右边，移动左边,因为要判断[i+1,j-1],[i+1,j-1]必须有有效值
        #如果固定左边，移动右边，则不能保证[i+1][j-1]处有有效值
        for j in range(1,m):
            for i in range(0,j):
                if s[j] == s[i]:
                    #这个判断保证了次对角线元素的取值
                    if j-i<=2:
                        matrix[i][j]= True
                    else:
                        matrix[i][j]=matrix[i+1][j-1]
                    if matrix[i][j]:
                        if j-i+1>max_len:
                            max_len = j-i+1
                            max_s = s[i:(j+1)]
                else:
                    matrix[i][j] =False
        return max_s
        # 思路三：中心点扩散
        # m = len(s)
        # if m==1:
        #     return s
        # if m==2:
        #     if s[0]==s[1]:
        #         return s
        #     else:
        #         return s[0]
        # max_len=1
        # str_max_len = s[0]
        # for i in range(1,len(s)):
        #     left,right = i-1,i+1
        #     cur_len = 1
        #     #判断直接以当前一点向两边扩还是以当前两点向两边扩
        #     if left>=0 and right<len(s):
        #         if s[i]==s[left] and s[i]!=s[right]:
        #             cur_len = 2
        #             left = i-2
        #             if cur_len>max_len:
        #                 max_len = cur_len
        #                 str_max_len = s[(i-1):(i+1)]
        #         elif s[i]!=s[left] and s[i]==s[right]:
        #             cur_len = 2
        #             right = i+2
        #             if cur_len>max_len:
        #                 max_len = cur_len
        #                 str_max_len = s[i:(i+2)]
        
        #     while left>=0 and right<len(s):
        #         if s[left]==s[right]:
        #             cur_len+=2
        #             if cur_len>max_len:
        #                 max_len = cur_len
        #                 str_max_len = s[left:(right+1)]
        #             left-=1
        #             right+=1
        #         else:
        #             break
        # return str_max_len  


        


   
# @lc code=end

