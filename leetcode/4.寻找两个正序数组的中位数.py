#
# @lc app=leetcode.cn id=4 lang=python3
#
# [4] 寻找两个正序数组的中位数
#

# @lc code=start
class Solution:
    # 类似合并链表,一边合并一边判断是否到了中位数的位置
    # 需要注意的是把所有情况都考虑进去，例如有个数组为空，
    # 两个数组长度之和为奇数还是偶数，不同情况下如何处理
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        nums1_len = len(nums1)
        nums2_len = len(nums2)
        if nums1_len == 0 and nums2_len==0:
            return
        elif nums1_len == 0 and nums2_len!=0:
            if nums2_len%2 == 0:
                return (nums2[nums2_len//2-1]+nums2[nums2_len//2])/2
            else:
                return nums2[nums2_len//2]
        elif nums1_len !=0 and nums2_len ==0:
            if nums1_len%2 == 0:
                return (nums1[nums1_len//2-1]+nums1[nums1_len//2])/2
            else:
                return nums1[nums1_len//2]

        if (nums1_len+nums2_len)%2 == 0:
            median_loc = [(nums1_len+nums2_len)//2-1,(nums1_len+nums2_len)//2]
        else:
            median_loc = (nums1_len+nums2_len)//2
        i = 0
        j = 0
        loc = -1
        nums_sort = []
        median_value = -1
        while i < nums1_len and j < nums2_len:
            if nums1[i]<nums2[j]:
                nums_sort.append(nums1[i])
                i+=1
            else:
                nums_sort.append(nums2[j])
                j+=1
            loc+=1
            if isinstance(median_loc,list):
                if loc in median_loc and median_value!=-1:
                    return (median_value+nums_sort[-1])/2
                elif loc in median_loc and median_value==-1:
                    median_value = nums_sort[-1]
            #这个判断别忘了
            else:
                if loc == median_loc:
                    return nums_sort[-1]  
        while i<nums1_len:
            nums_sort.append(nums1[i])
            i+=1
            loc+=1
            if isinstance(median_loc,list):
                if loc in median_loc and median_value!=-1:
                    return (median_value+nums_sort[-1])/2
                elif loc in median_loc and median_value==-1:
                    median_value = nums_sort[-1]  
            #这个判断别忘了
            else:
                if loc == median_loc:
                    return nums_sort[-1]  
        while j<nums2_len:
            nums_sort.append(nums2[j])
            j+=1
            loc+=1
            if isinstance(median_loc,list):
                if loc in median_loc and median_value!=-1:
                    return (median_value+nums_sort[-1])/2
                elif loc in median_loc and median_value==-1:
                    median_value = nums_sort[-1]
            #这个判断别忘了
            else:
                if loc == median_loc:
                    return nums_sort[-1]    
        return median_value

# @lc code=end

