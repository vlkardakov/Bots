s = input()
n = int(input())
ci = []
xi = []
last = [0] * 26
for i in range(n):
    c, x = input().split()
    ci.append(c)
    xi.append(int(x))
    last[ord(c) - ord('a')] = len(s) - 1
dp = [0] * (len(s) + 1)
for i in range(1, len(s) + 1):
    if s[i - 1] in ci:
        j = last[ord(s[i - 1]) - ord('a')]
        dp[i] = dp[j] + xi[ci.index(s[i - 1])] + xi[ci.index(s[i - 1])] - 1
    else:
        dp[i] = dp[i - 1] + s[:i].count(s[i - 1])
print(dp[-1])