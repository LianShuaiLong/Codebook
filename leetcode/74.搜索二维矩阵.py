#
# @lc app=leetcode.cn id=74 lang=python3
#
# [74] 搜索二维矩阵
#

# @lc code=start
class Solution:
    # 二维搜索:先找到理论上应该在的行
    # 然后在该行进行一维搜索
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])
        val_0_0 = matrix[0][0]
        val_m_1_n_1 = matrix[m-1][n-1]
        if val_0_0>target:
            return False
        if val_m_1_n_1<target:
            return False
        left = 0
        right = m-1
        while left<=right:
            val_left = matrix[left][0]
            val_right = matrix[right][0]
            mid = (left+right)//2
            if val_left==target:
                return True
            if val_right == target:
                return True
            val_mid = matrix[mid][0]
            if val_mid == target:
                return True
            else:
                if val_mid>target:
                    right = mid-1
                else:
                    left = mid+1
        idx = right
        left = 0
        right = n-1
        while left <=right:
            val_left = matrix[idx][left]
            val_right = matrix[idx][right]
            mid = (left+right)//2
            if val_left == target:
                return True
            if val_right == target:
                return True
            val_mid = matrix[idx][mid]
            if val_mid == target:
                return True
            else:
                if val_mid<target:
                    left = mid+1
                else:
                    right = mid-1
        return False


# @lc code=end

