#
# @lc app=leetcode.cn id=240 lang=python3
#
# [240] 搜索二维矩阵 II
#

# @lc code=start
class Solution:
    #与搜索二维矩阵I不同,搜索矩阵可以根据matrix[i][0]
    #与target的相对大小，确定target理论上应该所处的行
    #而这个不能确定，所有matrix[i][0]<target的i,都
    #有可能成为target所在的行
    # 时间复杂度mlogn,优化一下可以改为min(mlogn,nlogm)
    def binary_search(self,matrix:List[int],target:int):
        left = 0
        right = len(matrix)-1
        if target<matrix[left]:
            return False
        if target>matrix[right]:
            return False
        while left<=right:
            val_left = matrix[left]
            val_right = matrix[right]
            mid = (left+right)//2
            if target == val_left:
                return True
            if target == val_right:
                return True
            val_mid = matrix[mid]
            if target == val_mid:
                return True
            else:
                if val_mid>target:
                    right = mid-1
                else:
                    left = mid+1
        return False

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])
        val_0_0 = matrix[0][0]
        val_m_1_n_1 = matrix[m-1][n-1]
        if val_0_0>target:
            return False
        if val_m_1_n_1<target:
            return False
        res = False
        for i in range(m):
            val_i_0 = matrix[i][0]
            val_i_n_1 = matrix[i][n-1]
            if val_i_0<=target and target<=val_i_n_1:
                res = res or self.binary_search(matrix[i],target)
        return res

        
# @lc code=end

