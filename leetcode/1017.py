class Solution:
    def baseNeg2(self, N: int) -> str:
        res = ''
        while N:
            N, k = -(N // 2), N % 2
            res = str(k)+res
        return res if res else '0'

s1 = Solution()
print(s1.baseNeg2(1))