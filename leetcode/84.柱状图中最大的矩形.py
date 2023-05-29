#
# @lc app=leetcode.cn id=84 lang=python3
#
# [84] 柱状图中最大的矩形
#

# @lc code=start
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        #暴力求解方法,枚举高
        #会超时
        # max_area = 0
        # for i in range(len(heights)):
        #     if i == 0:
        #         j = i
        #         while j<len(heights):
        #             if heights[j]>=heights[i]:
        #                 j+=1
        #             else:
        #                 break
        #         area = heights[i]*(j-i)
        #         max_area = max(max_area,area)
        #     elif i==len(heights)-1:
        #         j =i
        #         while j>=0:
        #             if heights[j]>=heights[i]:
        #                 j-=1
        #             else:
        #                 break
        #         area = heights[i]*(i-j)
        #         max_area = max(area,max_area)
        #     else:
        #         j_left = i
        #         j_right = i
        #         while j_left>=0:
        #             if heights[j_left]>=heights[i]:
        #                 j_left-=1
        #             else:
        #                 break
        #         while j_right<len(heights):
        #             if heights[j_right]>=heights[i]:
        #                 j_right+=1
        #             else:
        #                 break
        #         area = (j_right-j_left-1)*heights[i]
        #         max_area = max(max_area,area)
        # return max_area  
        # 单调栈 时间复杂度从O(N^2)降到O(N):从左向右的时候每个元素只会进栈一次最多出栈一次；从右向左类似O(4N)=O(N),空间复杂度O(4N)=O(N)
        # 用空间换时间
        # 找左边界,找到左边第一个小于heights[i]的高度
        # 维护一个单调递增的栈，栈里面的元素是可能作为左边界的高度取值,height[j_0]<=height[j_1]<=heights[j_2]<=...<=heights[j_i]<=heights[i]<=heights[j_i+1]
        # 假如中间有一个不成立，即heights[j_m]>heights[j_m+1]那么heights[j_m]一定不会再栈里面，
        # 因为heights[j_m+1]把heights[j_m]给挡住了,heights[j_m]不可能作为 一个左边界
        # 对于一个新来的height,对栈进行移除操作，直到栈顶元素小于height，然后将新height入栈，同时求出左半边的宽度(左半边的面积)
        # 我们从左向右进行遍历就可以得到每个height左边界idx;同样的我们从右向左遍历就可以得到每个height的右边界的idx，进一步得到
        # 每一个height对应的最大高度
        left_stack = []#用于找左边界操作
        left_boundary = []#用于存放左边界
        right_stack = []#用于找右边界操作
        right_boundary = []#用于存放右边界
        for i in range(len(heights)):
            if len(left_stack)==0:
                left_boundary.append(-1)
                left_stack.append((i,heights[i]))
            else:
                # 找到左边第一个小于height[i]的位置，pop出去的都不可能作为当前点的左边界
                # 也不可能作为下一点的左边界，
                # 下一点的左边界只可能是当前点(下一点大于当前点)或者当前点的左边界以左的点(下一点小于当前点)
                while len(left_stack)>0 and left_stack[-1][1]>=heights[i]:
                    idx,h = left_stack.pop()
                idx = left_stack[-1][0] if len(left_stack)>0 else -1
                left_boundary.append(idx)
                left_stack.append((i,heights[i]))
        for j in range(len(heights)-1,-1,-1):
            if len(right_stack)==0:
                right_boundary.append(len(heights))
                right_stack.append((j,heights[j]))
            else:
                while len(right_stack)>0 and right_stack[-1][1]>heights[j]:
                    idx,h = right_stack.pop()
                idx = right_stack[-1][0] if len(right_stack)>0 else len(heights)
                right_boundary.append(idx)
                right_stack.append((j,heights[j]))
        max_area = 0
        for i in range(len(heights)):
            h = heights[i]
            l_b = left_boundary[i]
            r_b = right_boundary[len(heights)-1-i]
            area = h*(r_b-l_b-1)
            max_area = max(max_area,area)
        return max_area
        #进一步优化，从左向右找左边界的时候，是不是就可以知道其右边界
       




# @lc code=end

