#
# @lc app=leetcode.cn id=17 lang=python3
#
# [17] 电话号码的字母组合
#

# @lc code=start
class Solution:
    def help(self,digits,digit_letter,layer,res,cur):
        #不仅要元素回退，而且要layer回退
        #layer和cur都是引用赋值的方式，后续操作会影响当前的取值
        for s in digit_letter[digits[layer]]:
            cur.append(s)
            if len(cur)==len(digits):
                res.append(''.join(cur))
                layer-=1
            else:
                layer+=1
                self.help(digits,digit_letter,layer,res,cur)
                layer-=1
            cur.pop()
        return 

    def letterCombinations(self, digits: str) -> List[str]:
        digit_letter={
            '2':['a','b','c'],
            '3':['d','e','f'],
            '4':['g','h','i'],
            '5':['j','k','l'],
            '6':['m','n','o'],
            '7':['p','q','r','s'],
            '8':['t','u','v'],
            '9':['w','x','y','z']}
        if len(digits)==0:
            return []
        res = []
        cur = []
        layer = 0 
        self.help(digits,digit_letter,layer,res,cur)
        return res

# @lc code=end

