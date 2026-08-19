## Lecture 9 Recursion 递归
### Reading 1.7 Recursive Functions
如果一个函数的函数体直接或间接调用了函数本身，则该函数被称为递归函数。没有特殊语法，但要去理解。
核心：把一个问题拆分成多个小问题
```python
# 示例
def sum_digits(n):
	if n < 10:
		return n
	else:
		all_but_last, last = m // 10, n % 10
		return sum_didits(all_but_last) + last
```

#### 1.7.1 The Anatomy of Recursive Functions 剖析递归函数
递归函数通过逐步简化问题来表达计算。

```python
def fact(n):
	if n == 1:
		return n
	else:
		return fact(n - 1) * n

```

我们可以展开它，但是我们会把它视为函数抽象，我们不关心fact(n - 1)如何实现，我们只相信它能实现。学会识别递归函数递归函数的计算过程确实需要练习。

#### 1.7.2 Mutual Recursion 相互递归
一个递归过程被分为两个相互调用的函数

```python
def is_even:
	if n == 0;
		return True
	else:
		return is_odd(n-1)

def is_odd(n):
	if n == 0:
		return False
	else:
		return is_even(n-1)

# 转化为简单递归函数
def is_even(n):
	if n == 0:
		return True
	else:
		if (n-1) == 0:
			return False
		else:
			return is_even((n-1) - 1)
```

#### 1.7.3 Printing in Recursive Functions 过程可视化
```python
def cascade(n):
	if n < 10:
		print(n)
	else:
		print(n)
		cascade(n//10)
		print(n)

# 基础情况可能不是硬性要求
def cascade(n):
	print(n)
	if n >= 10:
		cascade(n//10)
		print(n)

# 一个鹅卵石游戏的相互递归示例
def play_alice(n):
	if n == 0:
		print("Bod wins!")
	else:
		play_bob(n-1)

def play_bob(n):
	if n == 0:
		print("Alice win!")
	elif is_even(n):
		play_alice(n-2)
	else:
		play_alice(n-1)
```

#### 1.7.4 Tree Recursion 树形递归
函数多次调用自身。

```python
def fib(n):
	if n == 1:
		return 0
	if n == 2:
		return 1
	else:
		return fib(n-2) + fib(n-1)
```

#### 1.7.5 Example: Partitions 示例：划分
```python
# define a function count_partitions(n, m), 返回使用不超过m的部分对n进行不同划分的数量
# 问题拆分：
# （1）：划分n-m
# （2）：使用不超过m-1的较小分量进行划分
def count_partitions(n, m):
	if n == 0:
		return 1
	elif n < 0:
		return 0
	elif m == 0:
		return 0
	else:
		return count_partitions(n-m, m) + count_partitions(n, m-1)
```

我们可以将树递归函数视为探索不同的可能性

### Lab02: Higher-Order Functions, Lambda Expressions
（这是2026-fall的，做着做着发现被关掉了，只能回去做2026-spring的，一些顺序可能产生一些错位）
```python
print(3) or '' 
# 3
# ''
# print的返回值是None，or是短路运算符，左为True直接返回左，否则返回右
```

```python
# 4. Composite Identity Function, Function composite_identity, 接受f和g两个函数，返回另一个具有单参数x的函数，返回的函数在f(g(x)) = g(f(x))时返回True，否则返回False
def composite_identity(f, g):
    def composit_identity_help(x):
        if f(g(x)) == g(f(x)):
            return True
        else:
            return False
    return composit_identity_help
```

```python
# 5. Count Cond: Function count_cond来泛化两个相似函数
# Predicate Function: 返回True / False
def count_cond(condition):
    def count_cond_help(n):
        num = 0
        for i in range(1, n+1):
            if condition(n, i):
                num += 1
        return num
    return count_cond_help
```

```python
# 6. String Transformer: 使用lambda完成函数
def caesar_generator(num, op):
    return lambda letter: num_to_letter(op(num, letter_to_num(letter)))
```

```python
# 7. 检查回文数
def is_palindrome(n):
    x, y = n, 0
    f = lambda: y * 10 + x % 10 
    while x > 0:
        x, y = x // 10, f()
    return y == n
```

### Disc03: Recursion
```python
# 1. Skip Factorial，跳跃阶乘
def skip_factorial(n):
    if n == 1 or n == 2:
        return n
    else:
        return n * skip_factorial(n-2)

# 2. swip, 从后往前打，再从前往后打
def swipe(n):
    """Print the digits of n, one per line, first backward then forward.

    >>> swipe(2837)
    7
    3
    8
    2
    8
    3
    7
    """
    if n < 10:
        print(n)
    else:
	    # 需要理解，递归前的代码在进入递归时执行，递归后的代码在从递归返回后执行
        print(n % 10)
        swipe(n // 10)
        print(n % 10)
# is_prime_recursive
def is_prime(n):
    def is_prime_help(k):
        if k == n:
            return True
        elif n % k == 0:
            return False
        return is_prime_help(k+1) 
        #如果把递归当成一个循环的替代，那么递归不仅可以从n到1，也能从1到n

    return is_prime_help(2)


```