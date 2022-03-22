#
# @lc app=leetcode.cn id=79 lang=python3
#
# [79] 单词搜索
#

# @lc code=start
class Solution:
    def dfs(self,board,i,j,word,idx,visited):
        visited[i][j]=1
        if idx == len(word)-1:
            return True
        else:
            m = len(board)
            n = len(board[0])
            res = False
            for loc in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
                loc_x = loc[0]
                loc_y = loc[1]
                if loc_x>=0 and loc_x<m and loc_y>=0 and loc_y<n and visited[loc_x][loc_y]==0:
                    if board[loc_x][loc_y]==word[idx+1]:
                        if self.dfs(board,loc_x,loc_y,word,idx+1,visited):
                            return True
            visited[i][j]=0
            return False

    def exist(self, board: List[List[str]], word: str) -> bool:
        #dfs+回溯算法
        m = len(board)
        n = len(board[0])
        visited=[[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if board[i][j]==word[0]:
                    if self.dfs(board,i,j,word,0,visited):
                        return True
        return False

# @lc code=end

