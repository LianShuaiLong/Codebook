#
# @lc app=leetcode.cn id=36 lang=python3
#
# [36] 有效的数独
#

# @lc code=start
from collections import defaultdict
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        m = len(board)
        n = len(board[0])
        col_dict=defaultdict(set)
        row_dict=defaultdict(set)
        region_dict=defaultdict(set)
        for i in range(m):
            for j in range(n):
                value = board[i][j]
                if value=='.':
                    continue
                if value not in col_dict:
                    col_dict[value].add(i)
                else:
                    if i in col_dict[value]:
                        return False
                    else:
                        col_dict[value].add(i)
                if value not in row_dict:
                    row_dict[value].add(j)
                else:
                    if j in row_dict[value]:
                        return False
                    else:
                        row_dict[value].add(j)
                region_idx = (i//3)*3+j//3
                if value not in region_dict:
                    region_dict[value].add(region_idx)
                else:
                    if region_idx in region_dict[value]:
                        return False
                    else:
                        region_dict[value].add(region_idx)
        return True

# @lc code=end

