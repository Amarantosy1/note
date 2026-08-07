## Lecture1
### glob & regular expression
glob 和 regular expression的区别：glob通配符，适合表达路径之类的概念；regular expression正则表达式，适合表达文本的概念
glob \* {} ?
glob is a very simple pattern language
regular expression is more complicated

### 常用
sed用来查找替换(内置了自己的编程语言)
grep用来找内容（not recursively default)；
find用来找文件(recursively default)
chmod用来更改权限

control+c to cancel

awk从半结构化数据中提取信息(内置了自己的编程语言)
| 管道
<> 文件重定向输入输出（即将文件作为输入内容/输出位置）
/>> to append

if 不是一个program，pipeline不是一个program，它们都是bash language的一部分

### question
cd 为何内置于shell中？
>因为外部程序无法改变父进程，也就是当前 Shell 的工作目录。

### bash编程
用于将一个功能单独存起来，需要的时候直接调用

### homework
>1. `ls` 的 `-l` 选项（flag）作用是什么？运行 `ls -l /` 并观察输出。每一行最前面的 10 个字符分别代表什么？（提示：`man ls`）

l选项表示更多信息（long），1个字符表示文件类型，9个字符表示权限（依次是所有者，所属组，其他用户）。
其中第一个字符：
/-   普通文件
d   目录
l   符号链接
c   字符设备
b   块设备
p   命名管道（FIFO）
s   Unix 域套接字

后面9个字符：r读，w写，x执行

> 2. 在命令 `find ~/Downloads -type f -name "*.zip" -mtime +30` 中，`*.zip` 是一个 「glob」。什么是 glob ？新建一个测试目录并创建一些文件，试试 `ls *.txt` 、`ls file?.txt` 、`ls {a,b,c}.txt` 等模式。参见 Bash 手册中的 [Pattern Matching](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html) 。

glob是shell根据一定的规则自动匹配文件名或路径名的机制
主要包括*，\[]，\{}，?（在fish中被弃用）
[[glob]]

> 3. `'单引号'`、`"双引号"` 和 `$'ANSI 引号'` 有什么区别？写一条命令，输出一个同时包含字面量 `$` 、`!` 和换行符的字符串。参见 [Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html) 。

|写法|主要行为|
|---|---|
|`'单引号'`|内容几乎完全按字面量处理，`$`、`!`、`\n` 都不会被解释；单引号内部不能直接包含单引号|
|`"双引号"`|保留空格和换行，但仍会进行 `$变量`、`$(命令)` 等展开；在 Bash 交互模式中，`!` 还可能触发历史展开|
|`$'ANSI-C 引号'`|解析 `\n`、`\t`、`\x41`、`\u4e2d` 等转义序列；普通的 `$` 和 `!` 通常按字面量处理|

> 4. Shell 有三条标准流：stdin（0）、stdout（1）、stderr（2）。运行 `ls /nonexistent /tmp` ，把 stdout 和 stderr 分别重定向到两个文件。你将如何把两者都重定向到同一个文件？参见 [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) 。

分别重定向
```bash
ls /nonexistent /tmp >stdout.txt 2>stderr.txt
```
重定向到一个文件
```bash
ls /nonexistent /tmp >output.txt 2>&1
```

0: stdin
1: stdout
2: stderr
`&>` 是一个整体的重定向运算符，把2追加到1的地址里

> 5. `$?` 保存上一条命令的退出状态（0 表示成功）。`&&` 仅在前一条成功时执行后一条；`||` 仅在前一条失败时执行后一条。写一个一行命令：仅当 `/tmp/mydir` 不存在时才创建它。参见 [Exit Status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html) 。

```bash
ls /tmp/mydir || mkdir /tmp/mydir

mkdir -p /tmp/mydir % 常用写法

test -d /tmp/mydir || mkdir /tmp/mydir
```

> 6. 写一个脚本，接收文件名参数（`$1`），用 `test -f` 或 `[ -f ... ]` 检查该文件是否存在，并根据结果输出不同提示。参见 [Bash Conditional Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html) 。
> 7. 把上一题完成的脚本保存为文件（如 `check.sh`）。先运行 `./check.sh somefile` ，会发生什么？然后执行 `chmod +x check.sh` 再试一次。为什么这一步是必须的？（提示：比较 `chmod` 前后的 `ls -l check.sh` 输出）


```bash
#!/bin/bash

if [ -f "$1" ]; then
    echo "文件存在：$1"
else
    echo "文件不存在：$1"
fi
```

> 8. 在脚本的 `set` 选项（flag）里加入 `-x` 会发生什么？写个简单脚本试试并观察输出。参见 [The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) 。

会追踪命令的展开
```bash
#!/usr/bin/env bash

set -x

name="Mike"
count=2

echo "Hello, $name"

if [ "$count" -gt 1 ]; then
    echo "count 大于 1"
fi

set +x

echo "追踪已关闭"
```

> 9. 写一条命令，把文件复制为带当天日期的备份文件名（例如 `notes.txt` → `notes_2026-01-12.txt`）。（提示：`$(date +%Y-%m-%d)`）参见 [Command Substitution](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html)


```bash
cp note.txt "note_$(date +%Y-%m-%d).txt"
```

> 10. 修改讲义中的「复现偶尔才会失败的测试」脚本（flaky test），使它能够从命令行参数接收测试命令，而不是在脚本中写死 `cargo test my_test`。（提示：`$1` 或 `$@`）参见 [Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) 。

```bash
#!/bin/bash
set -euo pipefail

# Start CPU stress in background
stress --cpu 8 &
STRESS_PID=$!

# Setup log file
LOGFILE="test_runs_$(date +%s).log"
echo "Logging to $LOGFILE"

# Run tests until one fails
RUN=1
while cargo test my_test > "$LOGFILE" 2>&1; do # "$@"
    echo "Run $RUN passed"
    ((RUN++))
done

# Cleanup and report
kill $STRESS_PID
echo "Test failed on run $RUN"
echo "Last 20 lines of output:"
tail -n 20 "$LOGFILE"
echo "Full log: $LOGFILE"
```


> 11. 使用管道找出你「home 目录」中最常见的 5 种文件扩展名。（提示：组合 `find` 、`grep` / `sed` / `awk`、`sort`、`uniq -c` 以及 `head`）

> 12. `xargs` 会把 stdin 的每一行转换为命令参数。结合 `find` 和 `xargs`（不要用 `find -exec`），找出目录中所有 `.sh` 文件，并用 `wc -l` 统计每个文件行数。加分项：正确处理文件名中的空格。（提示：`-print0` 和 `-0`）参见 `man xargs` 。


```bash
find . -type f -name '*.sh' -print0 | xargs -0 wc -l
```

> 13. 使用 `curl` 获取 [课程网站](https://missing.csail.mit.edu/) 的 HTML，并通过 `grep` 统计列出了多少讲。（提示：找出每讲课程名称在那份 HTML 中的共性；用 `curl -s` 关闭进度输出。）

```bash
curl https://missing.csail.mit.edu/ | grep 'a ref="/2026' | wc -l
```

> 14. [`jq`](https://jqlang.github.io/jq/) 是处理 JSON 的强大工具。用 curl 获取示例数据 https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json，再用 jq 提取 version 大于 6 的人员姓名。（提示：先 `jq` . 看结构；再试 `jq '.[] | select(...) | .name'`）

```bash
cat demos.json | jq '.[] | select(version>=6) | .name'
```

> 15. `awk` 可以按列值过滤行并改写输出。例如，`awk '$3 ~ /pattern/ {$4=""; print}'` 会只输出第三列匹配 `pattern` 的行，并省略第四列。请写一个 `awk` 命令：只输出第二列大于 100 的行，并交换第一列和第三列。可用这条命令测试：`printf 'a 50 x\nb 150 y\nc 200 z\n'`

```bash

```


---
## lecture 2 命令行环境
需要知道的几个概念
- 参数（Arguments）
- 流（Streams）
- 环境变量（Environment variables）
- 返回码（Return codes）
- 信号（Signals）

### 1、参数
Shell的参数本质是纯字符串，由程序决定如何解析这些字符串
通过$可以访问参数，$1访问第一个参数，\$@以列表形式访问所有参数，\$# 获取参数个数，\$0获取程序本身名称
语法糖：支持传入不定数量的同类型参数，对每个参数执行相同操作。➡️配合通配符使用
```bash
## 通配符的理解

touch folder/{a,b,c}.py
# 会被扩展为
touch folder/a.py folder/b.py folder/c.py

convert image.{png,jpg}
# 会被扩展为
convert image.png image.jpg

cp /path/to/project/{setup,build,deploy}.sh /newpath
# 会被扩展为
cp /path/to/project/setup.sh /path/to/project/build.sh /path/to/project/deploy.sh /newpath

# 通配符技巧也可以被结合
mv *{.py,.sh} folder
# 会移动所有 *.py 和 *.sh 文件
```

### 2、流
管道中的所有程序是并发的
输入流：stdin
输出流：stdout，stderr
```bash
## 关于文件的重定向
# 将标准输出（stdout）重定向到文件（覆盖）
echo "hello" > output.txt

# 将标准输出（stdout）重定向到文件（追加）
echo "world" >> output.txt

# 将标准错误（stderr）重定向到文件
ls foobar 2> errors.txt

# 将标准输出和标准错误同时重定向到同一个文件
ls foobar &> all_output.txt

# 从文件中重定向标准输入（stdin）
grep "pattern" < input.txt

# 通过重定向到 /dev/null 来丢弃输出
cmd > /dev/null 2>&1
```

fzf：模糊查找，从stdin中逐行读取输入，提供交互式界面筛选和选择
### 3、环境变量
在shell中，空格的作用是分隔参数。
shell变量没有类型，本质上全部都是字符串。
把一个命令的输出保存到变量里：使用命令替换
```bash
files=$(ls)
echo "$files" | grep README
echo "$files" | grep ".py"
```

当shell调用别的程序时，会同时传入环境变量

特性：进程替换，`<(command)`把输出存入临时文件，在某个程序只接受文件作为输入时很有用
`printenv`打印当前环境变量
### 4、返回码
表示程序运行结束状态，0表示一切正常，非0表示执行中遇到了问题
Shell中的`&&`和`||`分别表示`And`和`Or`，Shell中的这两个运算符基于程序的返回码工作
在shell的`if`中，0表示True，非0表示False
### 5、信号
信号的本质是一种软件终端，如，按下`control+c`时，会给shell一个中断当前进程的信号
```bash
$ sleep 1000
^Z
[1]  + 18653 suspended  sleep 1000

$ nohup sleep 2000 &
[2] 18745
appending output to nohup.out

$ jobs
[1]  + suspended  sleep 1000
[2]  - running    nohup sleep 2000

$ kill -SIGHUP %1
[1]  + 18653 hangup     sleep 1000

$ kill -SIGHUP %2   # nohup 防止 SIGHUP

$ jobs
[2]  + running    nohup sleep 2000

$ kill %2
[2]  + 18745 terminated  nohup sleep 2000
```

### 6、远程机器
ssh(secure shell)
```bash
# 这里 ls 在远程执行，wc 在本地执行
ssh alice@server ls | wc -l

# 这里 ls 和 wc 都在远程服务器上执行
ssh alice@server 'ls | wc -l'
```
ssh还可以非交互式地执行命令

### 7、终端复用器
终端复用器允许同时操控多个shell会话，不再需要nohup技巧

### 8、定制shell
shell本身是通过dotfiles配置的程序之一
```bash
## alias的相关用法
# 为常用选项制作简写
alias ll="ls -lh"

# 节省大量输入常用命令的时间
alias gs="git status"
alias gc="git commit"

# 避免输入错误
alias sl=ls

# 覆盖现有命令以获得更好的默认值
alias mv="mv -i"           # -i 覆盖前提示
alias mkdir="mkdir -p"     # -p 根据需要创建父目录
alias df="df -h"           # -h 打印人类可读的格式

# 可以组成别名
alias la="ls -A"
alias lla="la -l"

# 要忽略别名，请运行它并在其前面加上 \
\ls
# 或者使用 unalias 完全禁用别名
unalias la

# 要获取别名定义，只需使用 alias 调用它
alias ll
# 将打印 ll='ls -lh'
```

如何配置自己的dotfiles
>推荐的做法是：放在一个单独的目录里，纳入版本控制，再用脚本通过**符号链接（symlink）** 链接到实际位置。好处如下：
>- **安装方便**：登录到一台新机器时，应用这些配置只需要一分钟。
>- **可移植性**：无论在哪台机器上，工具的行为都尽量保持一致。
>**便于同步**：你可以在任何地方更新 dotfiles，并让它们始终保持同步。
>- **变更可追踪**：你大概率会在整个职业生涯中一直维护这些 dotfiles，而长期项目保留版本历史总是件好事。

### 9、shell中的AI

### homework
> 1. 你可能见过像 `cmd --flag -- --notaflag` 这样的命令。这里的 `--` 是一个特殊参数，它告诉程序后面不要再继续解析选项（flag）了。也就是说，`--` 后面的所有内容都会被当作位置参数（positional argument）。这有什么用？试着运行 `touch -- -myfile`，然后在不使用 `--` 的情况下把它删掉。

```bash
rm ./-myfile
```

> 2. 进程替换 `<(command)` 可以让你把一个命令的输出当成文件来用。试着配合 `diff` 和进程替换，比较 `printenv` 与 `export` 的输出。它们为什么不一样？（提示：可以试试 `diff <(printenv | sort) <(export | sort)`）

fish中使用`psub`进行进程替换
```bash
diff (printenv | sort | psub) (export | sort | psub)
```

> 3. 写两个 bash 函数 `marco` 和 `polo`，行为如下：每次执行 `marco` 时，都要以某种方式保存当前工作目录；之后无论你切到哪个目录，只要执行 `polo`，它都应该把你 `cd` 回执行 `marco` 时所在的目录。为了方便调试，你可以把代码写进 `marco.sh`，然后通过执行 `source marco.sh` 把这些定义重新加载到当前 shell。

```bash
## fish版本
function marco
    set -g MARCO_DIR $PWD
    printf '已保存目录：%s\n' "$MARCO_DIR"
end

function polo
    if not set -q MARCO_DIR
        echo '错误：尚未执行 marco' >&2
        return 1
    end

    cd -- "$MARCO_DIR"
end
```

> 4. 假设你有一个很少失败的命令。为了调试它，你需要把它的输出保存下来，但等到一次失败运行可能会很耗时。写一个 bash 脚本，不断运行下面这个脚本直到它失败为止，并把标准输出和标准错误分别保存到文件里，最后把结果打印出来。如果你还能顺便报告它运行了多少次才失败，就加分。

```bash
#!/bin/bash 
count=1 
while ./test_fail.sh >stdout.log 2>stderr.log; do 
	((count ++)) 
done 
echo "第 $count 次运行失败" 
cat stdout.log 
cat stderr.log
```