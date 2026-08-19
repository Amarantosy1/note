## Disc02
```python
def make_keeper(n):
    def f(cond):
        for i in range(1, n+1):
            if cond(i):
                print(i)
    return f


def match_k(k):
    def check(x):
        while x // (10 ** k) > 0:
            if (x // 10 ** k) % 10 != x % 10:
                return False
            x //= 10
        return True
    return check

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return- 1
    else:
        return 0
    
def ramp(n):
    n, last, tally = n // 10, n % 10, 0

    while n:
        n, last, tally = n // 10, n % 10, tally + sign(last - n%10)
    return tally > 0
    
def process(n, tally, result):
    while n >= 10:
        tally, result = tally(n % 100 // 10, n % 10)
        n = n // 10
    return result()

def ups(k):
    def f(left, right):
        return ups(min(k, k + sign(left - right))) 
    # 递归你赢了
    return f, lambda: k == 0

def only(n, t):
    keep = 0
    while n:
        n, d = n // 10, n % 10
        if t(d):
            keep = 10 * keep + d
    while keep:
        n, keep = keep % 10 + n * 10, keep // 10
    return n
    
def every(t):
    def digit(n):
        while n:
            if not t(n % 10):
                return False
            n = n // 10
        return True
    return digit
```
