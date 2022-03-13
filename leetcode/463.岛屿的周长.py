#
# @lc app=leetcode.cn id=463 lang=python3
#
# [463] 岛屿的周长
#

# @lc code=start
class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        island_loc = set()#i,j,direction:0:竖向，1:横向
        for i in range(m):
            for j in range(n):
                if grid[i][j] ==1:
                    i_j_direc1 = (i,j,0)
                    i_j_direc2 = (i,j,1)
                    i_j_direc3 = (i+1,j,1)
                    i_j_direc4 = (i,j+1,0)
                    if i_j_direc1 not in island_loc:
                        island_loc.add(i_j_direc1)
                    else:
                        island_loc.remove(i_j_direc1)
                    if i_j_direc2 not in island_loc:
                        island_loc.add(i_j_direc2)
                    else:
                        island_loc.remove(i_j_direc2)
                    if i_j_direc3 not in island_loc:
                        island_loc.add(i_j_direc3)
                    else:
                        island_loc.remove(i_j_direc3)
                    if i_j_direc4 not in island_loc:
                        island_loc.add(i_j_direc4)
                    else:
                        island_loc.remove(i_j_direc4)
        return len(island_loc)

# @lc code=end

