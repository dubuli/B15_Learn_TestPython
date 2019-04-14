# Definition for singly-linked list.
# 如果在列表中,

from typing import List

class ListNode():
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution:
    def nextLargerNodes(self, head: ListNode) -> List[int]:
        if not head:
            return []
        if not head.next:
            return [0]
        
        nums = []
        while head:
            nums.append(head.val)
            head = head.next
            
        ret = [0] * len(nums)
        stack = []
        for i in range(len(nums)):
            while stack and nums[stack[-1]] < nums[i]:
                ret[stack.pop()] = nums[i]
            stack.append(i)
            
        return ret


s1 = Solution()
ln1 = ListNode(1)
ln2 = ListNode(2)
ln3 = ListNode(3)
ln4 = ListNode(2)
ln5 = ListNode(3)
ln6 = ListNode(4)
ln7 = ListNode(3)

ln1.next = ln2
ln2.next = ln3
ln3.next = ln4
ln4.next = ln5
ln5.next = ln6
ln6.next = ln7

r1 = s1.nextLargerNodes(ln1)
print(r1)