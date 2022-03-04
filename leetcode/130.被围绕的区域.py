#
# @lc app=leetcode.cn id=130 lang=python3
#
# [130] 被围绕的区域
#
# https://leetcode-cn.com/problems/surrounded-regions/description/
#
# algorithms
# Medium (45.27%)
# Likes:    736
# Dislikes: 0
# Total Accepted:    155.5K
# Total Submissions: 343.4K
# Testcase Example:  '[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]'
#
# 给你一个 m x n 的矩阵 board ，由若干字符 'X' 和 'O' ，找到所有被 'X' 围绕的区域，并将这些区域里所有的 'O' 用 'X'
# 填充。
# 
# 
# 
# 
# 示例 1：
# 
# 
# 输入：board =
# [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
# 输出：[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
# 解释：被围绕的区间不会存在于边界上，换句话说，任何边界上的 'O' 都不会被填充为 'X'。 任何不在边界上，或不与边界上的 'O' 相连的 'O'
# 最终都会被填充为 'X'。如果两个元素在水平或垂直方向相邻，则称它们是“相连”的。
# 
# 
# 示例 2：
# 
# 
# 输入：board = [["X"]]
# 输出：[["X"]]
# 
# 
# 
# 
# 提示：
# 
# 
# m == board.length
# n == board[i].length
# 1 
# board[i][j] 为 'X' 或 'O'
# 
# 
# 
# 
#

# @lc code=start
import queue
class Solution:
    def dfs(self,board,i,j):
        m = len(board)
        n = len(board[0])
        for loc in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
            loc_x = loc[0]
            loc_y = loc[1]
            if loc_x>=0 and loc_x<m and loc_y>=0 and loc_y<n and board[loc_x][loc_y]=='O':
                board[loc_x][loc_y] = 'o'
                self.dfs(board,loc_x,loc_y)
        return 

    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # bfs的方式
        # m = len(board)
        # n = len(board[0])
        # visit_cord = queue.Queue()
        # for i in range(m):
        #     if board[i][0]=='O':
        #         board[i][0]='o'#做标记
        #         visit_cord.put([i,0])
        #     if board[i][n-1] == 'O':
        #         board[i][n-1]='o'
        #         visit_cord.put([i,n-1])
        # for i in range(n):
        #     if board[0][i] == 'O':
        #         board[0][i]='o'
        #         visit_cord.put([0,i])
        #     if board[m-1][i] == 'O':
        #         board[m-1][i]='o'
        #         visit_cord.put([m-1,i])
        # while not visit_cord.empty():
        #     cord = visit_cord.get()
        #     cord_x = cord[0]
        #     cord_y = cord[1]
        #     for c in [[cord_x-1,cord_y],[cord_x+1,cord_y],[cord_x,cord_y-1],[cord_x,cord_y+1]]:
        #         c_x = c[0]
        #         c_y = c[1]
        #         if c_x>=0 and c_x<m and c_y>=0 and c_y<n and board[c_x][c_y]=='O':
        #             board[c_x][c_y] = 'o'
        #             visit_cord.put([c_x,c_y])
        # for i in range(m):
        #     for j in range(n):
        #         if board[i][j]=='o':
        #             board[i][j]='O'
        #         else:
        #             board[i][j]='X'
        # return 
        # dfs方式
        m = len(board)
        n = len(board[0])
        for i in range(m):
            if board[i][0] == 'O':
                board[i][0] = 'o'
                self.dfs(board,i,0)
            if board[i][n-1] == 'O':
                board[i][n-1] = 'o'
                self.dfs(board,i,n-1)
        for i in range(n):
            if board[0][i] == 'O':
                board[0][i] = 'o'
                self.dfs(board,0,i)
            if board[m-1][i] == 'O':
                board[m-1][i] = 'o'
                self.dfs(board,m-1,i)
        for i in range(m):
            for j in range(n):
                if board[i][j]=='o':
                    board[i][j]='O'
                else:
                    board[i][j]='X'
        return 
# @lc code=end

