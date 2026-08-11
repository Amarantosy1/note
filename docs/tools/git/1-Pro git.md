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
一个提交对象包含一个指向暂存内容快照的指针、作者的姓名和邮箱、提交信息、指向它的父对象的指针。
> 一个例子
> ![首次提交对象及其树结构。](https://git-scm.com/book/zh/v2/images/commit-and-tree.png)
> ![提交对象及其父对象。](https://git-scm.com/book/zh/v2/images/commits-and-parents.png)


Git 分支本质仅仅是指向提交对象的可变指针。`master`分支不是特殊分支，而是默认创建的，大家都懒得改变，就这样了。
![分支及其提交历史。](https://git-scm.com/book/zh/v2/images/branch-and-history.png)

#### 分支创建
```bash
git branch <branchname> #只是创建了一个可以移动的新的指针,HEAD是指向当前分支的特殊指针，可以想象成是当前所在分支的别名
git log --online --decorate #查看各个分支当前所指对象
git checkout <branchname> #讲HEAD切换到一个已存在的分支
git checkout -b <branchname> #创建一个新分支然后立刻切换过去

```

当在分支做了提交后，切换回`master`，工作目录的文件将变回旧的版本。
![项目分叉历史。](https://git-scm.com/book/zh/v2/images/advance-master.png)

当在不同分支作出修改并提交时，项目会产生分叉。

```bash
git log --oneline --decorate --graph --all #查看项目分叉历史
```

Git的分支实质只是一个校验和，创建一个分支相当于在文件内写入41个字节（40字符+1换行符），速度极快。

### 3.2 分支的新建与合并
```markdown
让我们来看一个简单的分支新建与分支合并的例子，实际工作中你可能会用到类似的工作流。 你将经历如下步骤：

1. 开发某个网站。
    
2. 为实现某个新的用户需求，创建一个分支。
    
3. 在这个分支上开展工作。
    

正在此时，你突然接到一个电话说有个很严重的问题需要紧急修补。 你将按照如下方式来处理：

1. 切换到你的线上分支（production branch）。
    
2. 为这个紧急任务新建一个分支，并在其中修复它。
    
3. 在测试通过之后，切换回线上分支，然后合并这个修补分支，最后将改动推送到线上分支。
    
4. 切换回你最初工作的分支上，继续工作。
```

#### 新建分支
初始状态
![一个简单的提交历史。](https://git-scm.com/book/zh/v2/images/basic-branching-1.png)

```bash
git checkout -b iss53
```

![创建一个新分支指针。](https://git-scm.com/book/zh/v2/images/basic-branching-2.png)

```bash
#作出修改然后
git commit -a -m "added sth"
```

![`iss53` 分支随着工作的进展向前推进。](https://git-scm.com/book/zh/v2/images/basic-branching-3.png)

```bash
#遇到紧急情况
git checkout -b hotfix
#作出一些修改然后
git commit -a -m 'fixed bugs'
```

![基于 `master` 分支的紧急问题分支（hotfix branch）。](https://git-scm.com/book/zh/v2/images/basic-branching-4.png)

```bash
#测试之后合并
git checkout master
git merge hotfix #会出现Fast-forward，合并操作
```

![`master` 被快进到 `hotfix`。](https://git-scm.com/book/zh/v2/images/basic-branching-5.png)

```bash
#删除不需要的分支
git branch -d hotfix
#切换回原分支
git checkout iss53
#作出一些修改然后提交
git commit -a -m 'do sth'
```

![继续在 `iss53` 分支上的工作。](https://git-scm.com/book/zh/v2/images/basic-branching-6.png)

```bash
#合并分支
git checkout master
git merge iss53 #recursive strategy
```

![一次典型合并中所用到的三个快照。](https://git-scm.com/book/zh/v2/images/basic-merging-1.png)
![一个合并提交。](https://git-scm.com/book/zh/v2/images/basic-merging-2.png)


```bash
git branch -d iss53 #删除分支
```

#### 产生冲突的合并
解决文件冲突之后使用`git add`来标记冲突已解决
`git mergetool`可以启用图形化工具一步步解决冲突。

### 3.3 分支管理
```bash
git branch -v #查看每个分支的最后一次提交
git branch --merged #查看已经合并了的分支
git branch --no-merged #查看包含未合并工作分支
git branch -D <branchname> #强制删除并放弃未合并内容
```

### 3.4 分支开发工作流
#### 长期分支
可以同时拥有多个开放的分支。稳定分支的指针总是在提交历史中落后一大截，前沿分支往往比较靠前。
使用多个长期分支对于大型项目很有用
#### 主题分支
![拥有多个主题分支的提交历史。|380x301](https://git-scm.com/book/zh/v2/images/topic-branches-1.png)
![合并了 `dumbidea` 和 `iss91v2` 分支之后的提交历史。](https://git-scm.com/book/zh/v2/images/topic-branches-2.png)

### 3.5 远程分支
远程引用：对远程仓库的引用
```bash
git ls-remote <remote> #获取远程引用完整列表
```

远程追踪分支：远程分支状态的引用

![克隆之后的服务器与本地仓库。](https://git-scm.com/book/zh/v2/images/remote-branches-1.png)

clone了一个repo到本地

![本地与远程的工作可以分叉。](https://git-scm.com/book/zh/v2/images/remote-branches-2.png)
别人push了东西到服务器，先`fetch`，然后会更新本地数据

![`git fetch` 更新你的远程仓库引用。](https://git-scm.com/book/zh/v2/images/remote-branches-3.png)
这时，又clone了一个仓库

![添加另一个远程仓库。](https://git-scm.com/book/zh/v2/images/remote-branches-4.png)
![远程跟踪分支 `teamone/master`。](https://git-scm.com/book/zh/v2/images/remote-branches-5.png)


#### 推送
```bash
git push origin serverfix #serverfix被展开为refs/heads/serverfix:refs/heads/serverfix
git merge origin/serverfix #如果是抓到了别人的更新，则不会自动拷贝文件，需要自己merge到当前分支
git checkout -b serverfix origin/serverfix #创建一个用于工作的本地分支
```

#### 追踪分支
跟踪分支是与远程分支有直接关联的本地分支
```bash
git pull #自动识别抓取合并
git checkout --track origin/serverfix #
git branch -vv #查看设置的所有追踪分支

```
#### 拉取
```bash
git fetch #从服务器拉取数据但不合并
git pull #从服务器拉取数据并自动合并，相当于git fetch + git merge
```
#### 删除远程分支
```bash
git push origin --delete serverfix
```

### 3.6 变基
整合分支的两个办法：`merge`和`rebase`
#### 变基的基本操作
`merge`把两个分支的最新快照以及二者最近的共同祖先进行三方合并，生成一个新的快照（并提交）
`rebase`变基，把对某一分支上的所有修改移至另一分支上
```bash
git rebase <basebranch> <topicbranch>
```

![通过合并操作来整合分叉了的历史。](https://git-scm.com/book/zh/v2/images/basic-rebase-2.png)

上图为`merge`的效果

```bash
# rebase
git checkout experiment
git rebase master #原理：找到两个分支最近共同祖先，把当前分支的修改存为临时文件，将当前分支指向目标基底，最后将临时文件的修改应用
```

![将 `C4` 中的修改变基到 `C3` 上。](https://git-scm.com/book/zh/v2/images/basic-rebase-3.png)

```bash 
git checkout master
git merge experiment
```

![`master` 分支的快进合并。](https://git-scm.com/book/zh/v2/images/basic-rebase-4.png)

变基和三方合并的结果没有区别，不同在于提交历史，变基会使提交历史更加简洁
#### 更有趣的变基例子
```bash
git rebase --onto master server client
```
![[1-Pro git-1786246663753.webp]]

#### 变基的风险
原则：如果提交存在于你的仓库之外，而别人可能基于这些提交进行开发，那么不要执行变基
变基的实质是丢弃一些现有的提交，然后相应地新建一些内容一样但实质上不同的提交。
#### 用变基解决变基
如果真的出现了问题：团队中的某个人强制推送并覆盖了你所基于的提交，你需要做的事是检查你做了什么修改，以及他们覆盖了哪些修改。一般而言，使用`git pull --rebase` Git可以帮我们自动完成。
#### 变基vs合并（`rebase`vs`merge`）
一种观点是认为提交历史记录着发生过什么，本身就有很大的价值；另一种观点认为草稿作为提交历史会一团糟。没有一个简单的答案，根据实际来看。总的原则是，自己的东西可以变基，跟别人共享的不要变基。

## 4、服务器上的Git
本章对于没有服务器/搭建自己的Git服务器不感兴趣的同学可以直接跳过（先跳过）

## 5、分布式Git
### 5.1 分布式工作流程
#### 集中式工作流
广泛使用的工作流。
![[1-Pro git-1786256455639.webp]]

#### 集成管理者工作流
```markdown
# 工作流程
1. 项目维护者推送到主仓库。
    
2. 贡献者克隆此仓库，做出修改。
    
3. 贡献者将数据推送到自己的公开仓库。
    
4. 贡献者给维护者发送邮件，请求拉取自己的更新。
    
5. 维护者在自己本地的仓库中，将贡献者的仓库加为远程仓库并合并修改。
    
6. 维护者将合并后的修改推送到主仓库。
```

GitHub最常用的工作流程
#### 主管与副主管工作流
不常用，只有项目极为庞大复杂（如Linux内核项目）才会用到。

### 5.2 向一个项目贡献
贡献方式的影响因素：活跃贡献者的数量；项目使用的工作流程；提交权限

#### 提交准则
```bash
git diff --check #检查空白错误，提交不应该包含任何空白错误
git add --patch #使用add的交互式模式，让每次提交成为一个逻辑上的独立变更集
```

#### 提交信息如何撰写
```text
首字母大写的摘要（不多于 50 个字符）

如果必要的话，加入更详细的解释文字。在大概 72 个字符的时候换行。
在某些情形下，第一行被当作一封电子邮件的标题，剩下的文本作为正文。
分隔摘要与正文的空行是必须的（除非你完全省略正文），
如果你将两者混在一起，那么在使用例如变基这样的工具时，它们会生成难以阅读的输出，让人困惑。

使用指令式的语气来编写提交信息：使用“Fix bug”而非“Fixed bug”或“Fixes bug”。
此约定与 git merge 和 git revert 命令生成提交说明相同。

空行接着更进一步的段落。

- 标号也是可以的。

- 项目符号可以使用典型的连字符或星号，后跟一个空格，行之间用空行隔开，
  但是可以依据不同的惯例有所不同。

- 使用悬挂式缩进
```

#### 私有小型团队场景
![[1-Pro git-1786424980614.webp]]

#### 私有管理团队
员工通常不会有推送到`origin/main`的权限，跟同事共享工作需要推送到另一个分支
```bash
git push -u origin featureA
git push -u origin featureB:featureBee #当别人取的上游分支名字与你取的名字不一样时
```

![[1-Pro git-1786426001933.webp]]

#### 派生的公开项目
没有权限直接更新项目分支，必须使用其它办法将工作给维护者。
fork，pull-request，本地保持一个分支追踪`origin/main`

### 5.3 维护项目
```bash
# 先跳过这节，等有需求了再回来补
```

