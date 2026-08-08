## 1、起步
### 1.1 关于版本控制
版本控制记录内容变化
#### 本地版本控制系统
一种常见的方式是复制然后重命名v1 v2，但这很容易写错文件/覆盖文件。
为了解决这个问题，人们发明了许多本地版本控制系统，大多使用数据库记录文件历次更新差异。
#### 集中化的版本控制系统
另一个问题是协同开发。人们想到用服务器来保存仓库的所有版本，客户端连接到服务器以获取/提交更新。新的问题是服务器故障了会有丢失所有东西的风险。
#### 分布式版本控制系统
客户端不止提取最新版本文件快照，而是把仓库完整镜像。服务器故障了也可以使用任意本地克隆的仓库恢复。
### 1.2 Git简史
Linux内核开源项目，他们使用bitkeeper来管理和维护代码，然而，bitkeeper收回Linux内核社区免费使用的权利。所以他们自己开发了自己的版本系统Git。诞生于2005年（跟我差不多一个岁数呢）
### 1.3 Git是什么？
#### 直接记录快照，而非差异比较
其它大部分版本控制系统都是基于差异的版本控制
![存储每个文件与初始版本的差异。](https://git-scm.com/book/zh/v2/images/deltas.png)
git把数据看作对小型文件系统的一系列快照
![Git 存储项目随时间改变的快照。](https://git-scm.com/book/zh/v2/images/snapshots.png)
Git更像是一个小型的文件系统，提供许多以此为基础构建的超强工具。体现在Git 分支上
#### 近乎所有操作都是本地执行
#### Git保证完整性
Git中所有数据在储存前都计算校验和，然后以校验和来引用。不可能在Git不知情时更改文件/目录。
校验和的方式：SHA-1 hash。
Git数据库中保存的信息都是以文件内容的哈希值索引，而非文件名。
#### Git 一般只添加数据
Git几乎不会执行任何可能导致文件不可恢复的操作。
#### 三种状态

- committed
- modified
- staged

![工作区、暂存区以及 Git 目录。](https://git-scm.com/book/zh/v2/images/areas.png)

工作区：相当于是在finder看到的东西
暂存区：一个文件，保存下次将要提交的文件列表信息
Git仓库目录：保存项目元数据和对象数据库
基本的Git工作流程：

- 在工作区中修改文件
- 选择性暂存到暂存区
- 提交更新
### 1.4 命令行
只有在命令行中才能执行git的所有命令

### 1.5 安装Git
### 1.6 初次运行Git前的配置
git config配置文件
系统级、用户级、仓库级
#### 用户信息
设置用户名和邮箱地址，这些信息会写入每一次的提交中，提交不可更改。
#### 文本编辑器
```bash
git config --global core.editor vim #使用vim来进行配置
```
#### 检查配置信息
```bash
git config --list #列出所有配置
git config <key> #检查某项配置
```

### 1.7 获取帮助
```bash
# git manpage
git help <verb>
git <verb> --help
man git-<verb>

git <verb> -h #获取快速参考
```

## 2、Git基础
### 2.1 获取Git仓库
两种方式：
- 将尚未进行版本控制的本地目录转化为Git仓库
- 从服务器克隆一个Git仓库

#### 在已存在的目录中初始化仓库
```bash
git init
git add *.c
git add LICENSE
git commit -m 'initial project version'
```

#### 克隆现有的仓库
```bash
git clone <url>
```

Git支持多种数据传输协议：https, git, ssh

### 2.2 记录每次更新到仓库
![Git 下文件生命周期图。](https://git-scm.com/book/zh/v2/images/lifecycle.png)

#### 检查当前文件状态
```bash
 git status
```

#### 跟踪新文件
```bash
git add <files> #追踪新文件，如果是目录，则追踪该目录下的文件
```

修改原本就存在的文件也需要重新暂存
#### 状态简览
```bash
git status -s #git status --short
```

#### 忽略文件
.gitignore文件格式规范
- 所有空行或以#开头的行都会被Git忽略
- 可以使用标准的glob模式匹配，它会递归地应用在整个工作区
- 用`/`开头防止递归
- 用`/`结尾指定目录
- `!`取反

例子
```bash
# 忽略所有的 .a 文件
*.a

# 但跟踪所有的 lib.a，即便你在前面忽略了 .a 文件
!lib.a

# 只忽略当前目录下的 TODO 文件，而不忽略 subdir/TODO
/TODO

# 忽略任何目录下名为 build 的文件夹
build/

# 忽略 doc/notes.txt，但不忽略 doc/server/arch.txt
doc/*.txt

# 忽略 doc/ 目录及其所有子目录下的 .pdf 文件
doc/**/*.pdf
```

github的一个[gitignore列表](https://github.com/github/gitignore)
#### 查看已暂存和未暂存的修改
```bash
git diff #查看未暂存的文件具体修改了什么地方
git diff --staged #比对已暂存文件与最后一次提交的文件差异
git diff --cached #查看已暂存的文件的变化
```

#### 提交更新
```bash
git commit #写好提交说明，直接commit会启动默认编辑器编写提交消息
git commit -m "提交说明"
git commit -a -m "提交说明" #跳过使用暂存区直接提交，不过要小心
```

#### 移除文件
```bash
git rm #从暂存区移除文件
git rm -f #删除之前修改过或已经放到暂存区的文件
git rm --cached #让Git不再跟踪
git rm log/\*.log #通配符，使用反斜杠是因为不用Shell帮忙展开
```

#### 移动文件
Git 并不显式跟踪文件移动操作，也不会在元数据中体现重命名操作，但是能够推断出来。
```bash
git mv file_from file_to
```

### 2.3 查看提交历史
```bash
git log #按时间顺序列出所有提交，包括校验和、作者姓名、电子邮件、提交时间、提交说明
git log -p #--patch 显示每次提交引入的差异，-n参数限制显示数量
git log --stat # 在每次提交下面列出所有被修改的文件、有多少被修改、总结
git log --pretty=oneline #使用不同于默认格式的方式展示提交历史，online将每个提交放在一行显示，format可以定制记录的显示格式
git log --pretty=format:"%h %s" --graph
git log --since=2.weeks #列出最近两周的提交
git log -S <name> #筛选添加/删除某字符串的提交
```

|选项|说明|
|---|---|
|`-p`|按补丁格式显示每个提交引入的差异。|
|`--stat`|显示每次提交的文件修改统计信息。|
|`--shortstat`|只显示 --stat 中最后的行数修改添加移除统计。|
|`--name-only`|仅在提交信息后显示已修改的文件清单。|
|`--name-status`|显示新增、修改、删除的文件清单。|
|`--abbrev-commit`|仅显示 SHA-1 校验和所有 40 个字符中的前几个字符。|
|`--relative-date`|使用较短的相对时间而不是完整格式显示日期（比如“2 weeks ago”）。|
|`--graph`|在日志旁以 ASCII 图形显示分支与合并历史。|
|`--pretty`|使用其他格式显示历史提交信息。可用的选项包括 oneline、short、full、fuller 和 format（用来定义自己的格式）。|
|`--oneline`|`--pretty=oneline --abbrev-commit` 合用的简写。|

|选项|说明|
|---|---|
|`-<n>`|仅显示最近的 n 条提交。|
|`--since`, `--after`|仅显示指定时间之后的提交。|
|`--until`, `--before`|仅显示指定时间之前的提交。|
|`--author`|仅显示作者匹配指定字符串的提交。|
|`--committer`|仅显示提交者匹配指定字符串的提交。|
|`--grep`|仅显示提交说明中包含指定字符串的提交。|
|`-S`|仅显示添加或删除内容匹配指定字符串的提交。|
### 2.4 撤销操作

```bash
git commit --amend #提交完后发现漏了文件/提交信息写错了，替换提交，意义是不让“小修补”这种信息进入提交历史
git reset HEAD <file> #取消暂存
git checkout -- <file> #放弃修改，是一个危险的命令，该文件在本地任何的修改都会消失

```

> Git中任何已提交的东西都是可以恢复的，未提交的东西丢失后可能再也找不到。

### 2.5 远程仓库的使用
`origin`是Git给远程仓库服务器的默认名字。
```bash
git remote #查看远程仓库信息
git remote -v #查看读写远程仓库url
git remote add <shortname> <url> #添加一个新的远程仓库
git fetch <reponame> #拉去远程有但本地没有的信息
git pull #自动抓取后合并远程分支到当前分支
git push <remote> <branch> #推送
git remote show <remote> #查看一个远程仓库的更多信息
git remote rename <name_from> <name_to> #重命名远程仓库简写名
git remote remove <remote> #移除一个远程仓库

```

### 2.6 打标签
```bash
git tag #列出已有标签
git tag -l "" #按特定模式查找标签
git tag -a v1.4 -m "my version 1.4" #创建附注标签，附注标签是一个对象，有校验和
git tag v1.4-lw #创建轻量标签，轻量标签只是一个引用，不是一个对象
git tag -a v1.2 9fceb02 #给过去补标签
git push origin <tagname> #将标签推送到远程
git push origin --tags #将所有标签推送到远程
git tag -d <tagname> #删除本地仓库轻量标签
git push origin --delete <tagname> #删除远程标签
git checkout <tagname> #查看某个标签指向的文件版本，但会使仓库处于detached HEAD状态，需要当心

```

### 2.7 Git别名
```bash
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.br branch
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk' #将git visual定义为gitk的别名，也就是说，将外部命令定义到git中
```

## 3、Git分支
### 3.1 分支简介

