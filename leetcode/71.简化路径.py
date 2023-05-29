#
# @lc app=leetcode.cn id=71 lang=python3
#
# [71] 简化路径
#

# @lc code=start
class Solution:
    def simplifyPath(self, path: str) -> str:
        #非路径的情况 kong|.|..
        # ..需要切回到上一级
        # .和kong直接continue
        path_list = path.split('/')
        linux_path = []
        for p in path_list:
            if len(p)>0 and p!='.' and p!='..':
                linux_path.append(p)
            elif p=='.':
                continue
            elif p=='..':
                if len(linux_path)>0:
                    linux_path.pop()
                else:
                    continue
            else:
                continue
        return '/'+'/'.join(linux_path)
       
# @lc code=end

