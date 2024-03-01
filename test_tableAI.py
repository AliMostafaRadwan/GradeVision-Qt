class Solution:
    def isPalindrome(self, x: int) -> bool:
        
        xS = str(x)
        rev = xS[::-1]
        try:
            if int(rev) == x:
                print(True)
            else:
                print(False)
        except ValueError:
            print(False)
        

sol = Solution()
sol.isPalindrome(121)

