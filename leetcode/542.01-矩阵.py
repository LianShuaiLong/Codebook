#
# @lc app=leetcode.cn id=542 lang=python3
#
# [542] 01 矩阵
#
# https://leetcode-cn.com/problems/01-matrix/description/
#
# algorithms
# Medium (45.87%)
# Likes:    620
# Dislikes: 0
# Total Accepted:    88.2K
# Total Submissions: 192.3K
# Testcase Example:  '[[0,0,0],[0,1,0],[0,0,0]]'
#
# 给定一个由 0 和 1 组成的矩阵 mat ，请输出一个大小相同的矩阵，其中每一个格子是 mat 中对应位置元素到最近的 0 的距离。
# 
# 两个相邻元素间的距离为 1 。
# 
# 
# 
# 示例 1：
# 
# 
# 
# 
# 输入：mat = [[0,0,0],[0,1,0],[0,0,0]]
# 输出：[[0,0,0],[0,1,0],[0,0,0]]
# 
# 
# 示例 2：
# 
# 
# 
# 
# 输入：mat = [[0,0,0],[0,1,0],[1,1,1]]
# 输出：[[0,0,0],[0,1,0],[1,2,1]]
# 
# 
# 
# 
# 提示：
# 
# 
# m == mat.length
# n == mat[i].length
# 1 
# 1 
# mat[i][j] is either 0 or 1.
# mat 中至少有一个 0 
# 
# 
#

# @lc code=start
import queue
class Solution:
    # BFS分为两种情况
    # case1:Tree的BFS，是一种典型的单源BFS，只需要将root结点入队(或者放到list),然后无脑一层一层的遍历即可
    # case2:图的BFS(多源BFS),相比于Tree的BFS，需要将所有的源放入队列；另外，Tree是有向的，而图是无向的，所以
    # 图的BFS需要标记是否已经访问过，并且需要在入队之前进行标记
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        # 整体思路:矩阵里面所有0是第一层
        # 从第一层统一向外扩,每次扩1,新扩的位置放到队列尾部,作为后续BFS的起点
        m = len(mat)
        n = len(mat[0])
        visit_coordinate = queue.Queue()
        for i in range(m):
            for j in range(n):
                if mat[i][j]==0:
                    # 第一层BFS的起始点
                    visit_coordinate.put([i,j])
                else:
                    # 该点还没有访问过
                    mat[i][j] = -1
        while not visit_coordinate.empty():
            # 获取当前BFS的起始点，并从队列删除(队列中存储的是每一层BFS的起始点坐标)
            coordinate = visit_coordinate.get()
            c_x = coordinate[0]
            c_y = coordinate[1]
            for loc in [[c_x-1,c_y],[c_x+1,c_y],[c_x,c_y-1],[c_x,c_y+1]]:
                l_x = loc[0]
                l_y = loc[1]
                if l_x>=0 and l_x<m and l_y>=0 and l_y<n and mat[l_x][l_y]==-1:
                    # 对于没有访问过的点，将其进行赋值(标记为已访问)，并将其坐标入队，作为后续BFS的起始点
                    mat[l_x][l_y] = mat[c_x][c_y]+1
                    visit_coordinate.put([l_x,l_y])
        return mat
        
# @lc code=end

