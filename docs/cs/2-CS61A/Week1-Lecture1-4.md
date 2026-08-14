## Lecture 1 Welcome, Coding Environment, Functions and Exceptions
### Lab00: Getting started
```bash
#1.What would python do
python3 ok -q python-basics -u
```

```bash
#2.Implementing Functions
```

```bash
#3.Running tests
python3 ok
```

```bash
#check score locally
python3 ok --score
```

#### Python 实用的命令行选项
```bash
python3 -i lab00.py #交互式运行
python3 -m doctest lab00.py #运行doctests
```

## Lecture 2 Control-控制
### Dic0: Getting started
学习成功的关键：完成作业和题目，不要使用llm

## Lecture 3 Higher-Order Functions

### Lab1: Functions and Control

```python
# 1.编写函数：返回从n到n-k的乘积，k为0时返回1
def falling(n, k):
	result = 1
	right = n-k
	if k == 0:
		return result
	else:
		while n > right:
			result *= n
			n -= 1
	return result
```

```python
# 2.编写函数：打印[1, n]中能被k整除的整数，返回数量
def divisible_by_k(n, k):
	count = 0
	for i in range(1, n+1): # 前闭后开
		if i % k == 0:
			count += 1
			print(i)
	return count
```

```python
# 3. 编写函数：判断一个数字是否含有两个连续的8，如有则返回True，无返回False
def double_eights(n):
	while n >= 10:
		if n % 100 == 88:
			return True
		n //= 10
	return False
```

```python
# 4. 返回n的第k+1位，超过为0
def digit(n, k):
	return (n // pow(10, k)) % 10
```

```python
# 5. 返回三个数中第二大的数字
def middle(a, b, c):
	return a + b + c - min(a, b, c) - max(a, b, c)
```

```python
# 6. 返回y的各位数字之和
def sum_digits(y):
	result = 0
	while y != 0:
		result += (y % 10)
		y // 10
	return result
```

### Reading: 1.6 Higher-Order Functions
（有点忘记了，[复习一下](https://www.composingprograms.com/pages/16-higher-order-functions.html)）
函数是一种抽象方法，高阶函数就是操作函数的函数（接受函数为参数/返回函数），是新一层的抽象。
#### 1.6.1 函数作为参数
```python
def sum_naturals(n):
	'''计算从1到n的自然数之和'''
	total, k = 0, 1
	while k <= n:
		total, k = total + k, k += 1
	return total

def sum_cubes(n):
	'''计算1到n的自然数的立方和'''
	total, k = 0, 1
	while k <= n:
		total, k = total + k*k*k, k += 1
	return total

# 上述两个函数可以抽象为同一种模式
def <name>(n):
	total, k = 0, 1
	while k <= n:
		total, k = total + <term>(k), k + 1
	return total

# 新一层的抽象改写上述两函数
def summation(n, term):
	total, k = 0, 1
	while k <= n:
		total, k = total + term(k), k + 1
	return total

def cube(x):
	return x*x*x
def sum_cubes(n):
	retunr summation(n, cube)

```

#### 1.6.2 函数作为通用方法
```python
# 一个使用迭代法计算黄金比例的例子
def improve(update, close, guess=1):
	while not close(guess):
		guess = update(guess)
	return guess

def golden_update(guess):
	return 1/guess + 1

def square_close_to_successor(guess):
	return approx_eq(guess * guess, guess + 1)

def approx_eq(x, y tolerance = 1e - 3):
	return abs(x - y) < tolerance
	
phi = improve(golden_update, square_close_to_successor)

# 代码测试
from math import sqrt
phi = 1/2 + sqrt(5)/2
def improve_test():
	approx_phi = improve(golden_update, square_close_to_successor)
	assert approx_eq(phi, approx_phi), 'phi differs from its approximation'
```

#### 1.6.3 Defining Functions: Nested Definitions
即，让一些不会复用的抽象置于局部，让函数能继承父函数的参数。局部不会干扰外部，局部能够访问内部和外部。

```python
def average(x, y):
	return (x + y)/2
def sqrt(a):
	def sqrt_update(x):
		return average(x, a/x)
	def sqrt_close(x):
		return approx_eq(x * x, a)
	return improve(sqrt_update, sqrt_close)
```

#### 1.6.4 函数作为返回值
```python
# 一个例子
def square(x):
	return x * x
def successor(x):
	return x + 1
def compose1(f, g):
	def h(x):
		return f(g(x))
	return h
square_successor = compose1(square, successor)
result = square_successor(12) # 169
```

#### 1.6.6 Currying 柯里化
给定f(x, y)，可以定义g，使得g(x)(y)等价于f(x, y)。把一个函数先填充一个参数，暂存为另一个函数，这个函数只接受单个参数。
当一个高阶函数要求你传入一个一元函数，但你的实际逻辑依赖多个参数时，可以先通过柯里化把上下文中已经知道的参数固定下来，再把剩下的参数留给高阶函数传入。

```python
def curried_pow(x):
	def h(y):
		return pow(x, y)
	return h
def map_to_range(start, end, f):
	while start < end:
		print(f(start))
		start = start + 1
map_to_range(0, 10, curried_pow(2)) # 也就是说，我们需要一个只接受单个参数的函数，也是一个作用域的问题。

# 定义函数来自动化柯里化，以及反柯里化
def curry2(y): # 其实也就是再抽象一层出去
	def g(x):
		def h(y):
			return f(x, y)
		return h
	return g
def uncurry2(g):
	def f(x, y):
		return g(x)(y)
	return f
```

#### 1.6.7 Lambda Expressions
当我们定义一个函数却不想起名字时。
lambda的理解：`lambda x: f(g(x))` A function that takes x and returns f(g(x))

```python
def compose1(f, g):
	return lambda x: f(g(x))

compose1 = lambda f,g: lambda x: f(g(x))
```

lambda的历史由来J
> It may seem perverse to use lambda to introduce a procedure/function. The notation goes back to Alonzo Church, who in the 1930's started with a "hat" symbol; he wrote the square function as "ŷ . y × y". But frustrated typographers moved the hat to the left of the parameter and changed it to a capital lambda: "Λy . y × y"; from there the capital lambda was changed to lowercase, and now we see "λy . y × y" in math books and (lambda (y) (* y y)) in Lisp.

#### 1.6.8 抽象与一等函数
我们需要敏锐地抓住程序中潜在的抽象机会，将其推广。
一等公民：拥有最少限制的元素。可以被绑定到名称上，可以作为参数传递给函数，可以作为函数的返回值，可以被包含数据结构中。
python中的函数被赋予了一等公民的地位。

#### 1.6.9 函数装饰器
一种特殊的语法，在执行`def`语句时应用于高阶函数
```python
def trace(fn):
	def wrapped(x):
		print('-> ', fn, '(', x, ')')
		return fn(x)
	return wrapped

@trace
def triple(x):
	return 3 * x

```


### Homework1: Functions, Control, Higher-Order Functions
```python
# 1. 返回 A + |B|, 不能使用abs函数
from operator import add, sub
def a_plus_abs_b(a, b):
	if b < 0:
		f = sub
	else:
		f = add
	return f(a, b)
```

```python
# 2. hailstone: 从n开始打印冰雹序列，返回步数。n 为偶数，除2，n为奇数，乘3+1，最后会变为1
def hailstone(n):
	step = 1
	def is_even(k):
		return k % 2 == 0
	while n != 1:
		print(n)
		if is_even(n):
			n //= 2
			step += 1
		else:
			n = n * 3 + 1
			step += 1
	print(1)
	return step
```

```python
# 3. 返回term(1)*...*term(n)
def product(n, term):
	total = 1
	while n > 0:
		total, n = total * term(n), n - 1
	return total
```

```python
# 4. 函数重复器
# 一开始想到的写法，但是会有问题，内层函数可以直接读取外层函数作用域中的变量；如果想在内层函数里对这个变量进行重新赋值，就必须声明 `nonlocal`。
def make_repeater(f, n):
	def h(x):
		nonlocal n
		while n > 0:
			x = f(x)
			n -= 1
		return x
	return h
# gpt引导的写法，内层函数只访问外层参数，但不修改
def make_repeater(f, n):
	def h(x):
		for _ in range(n):
			x = f(x)
		return x
	return h
# 更好的高阶函数的解法
def make_repeater(f, n)
	def compose1(f, g):
		return lambda x: f(g(x))
	g = f
	for _ in range(n - 1): #n-1是因为前面已经定义过一次g = f了
		g = compose1(f, g)
	
	return g
	
```

```python
# 5. 返回n的除了它本身最大的因子
def largest_factor(n):
	max_factor = 1
	for i in range(2, n):
		max_factor = n // i
		return max_factor
	return max_factor
```

```python
# 6. 返回fuse(start, fuse(term(1), fuse(term(2)...))
def accumulate(fuse, start, n, term):
	n_s_result = 1 #这样会出现一个问题，乘法从1开始没问题，加法从1开始似乎也没问题，但如果term(1) != 1，那就有问题
	if n == 0:
		return start
	else:
		while n > 1:
			n_s_result, n = fuse(n_s_result, term(n)), n - 1
	return fuse(start, n_s_result)
# 更好的解法，从term(n)开始做fuse操作
def accumulate(fuse, start, n, term):
	n_s_result = term(n)
	if n == 0:
		return start
	else:
		while n > 1:
			n_s_result, n = fuse(n_s_result, term(n-1)), n-1
	return fuse(start, n_s_result)
	
# 使用accumulate实现product和summation
def summation_using_accumulate(n, term):
	return accumulate(add, 0, n, term)
def product_using_accumulate(n, term):
	return accumulate(mul, 1, n, term)
```

### Project1: Hog
[[Project1-hog]]项目是一个实现游戏的project，非常有意思。能学到函数和高阶函数的用法，抽象的意义。也是我的第一个手搓下来的project

### Dic1: Functions and control
```python
# 1. is Prime?
def is_prime(n):
	if n == 1:
		return False
	k = 2
	while k < n:
		if n % k == 0:
			return False
		k += 1
	return True
	
# 2. fizzbuzz
def fizzbuzz(n):
	for i in range(1, n+1):
        if i % 3 == 0 and i % 5 == 0:
            print("fizzbuzz")
        elif i % 3 == 0:
            print("fizz")
        elif i % 5 == 0:
            print("buzz")
        else:
            print(i)

# 3. Ordered Digits
def ordered_digits(x):
	if x < 10:
        return True
    while x > 10:
        l = x//10%10
        r = x % 10
        if l > r:
            return False
        x //= 10
    return True
    
# 4. 判断一个数字的位数中有多少个唯一的数字
def unique_digits(n):
    num = 1
    while n >= 10:
        if has_digit(n // 10, n % 10):
            num -= 1
        num += 1
        n //= 10
    return num
            
def has_digit(n, k):
    assert k >= 0 and k < 10
    while n > 0:
        if n % 10 == k:
            return True
        n //= 10
    return False
    
# 5. repeating: 一个数字是否由t位数重复出来
def repeating(t, n):
    if pow(10, t-1) > n:  # make sure n has at least t digits
        return False
    end = n % pow(10, t)
    rest = n
    while rest:
        if rest % pow(10, t) != end:
           return False
        rest = rest // pow(10, t)
    return True
```
