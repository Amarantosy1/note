---
created: 2026-07-10
---
## 前言
起因是一觉起来Claude账号被A➗封了。。

> 【似水流年·暑假】一觉起来被断崖😭 https://www.cc98.org/topic/6571728 复制本链接到浏览器或者打开【CC98】微信小程序查看~

然而我已经离不开Claude code了，先继续使用了一会Claude code接DeepSeek，但是效果不尽如人意，DeepSeek的模型能力确实只能说得上是勉强够用。目前来看，DeepSeek处理一些复杂问题就很难跟Claude/GPT相比。接着我又想到，能不能使用中转站继续使用Claude呢，尝试一下之后，发现，模型智力确实没啥大问题，就是好一点的中转站收费都不便宜，不太能承担得起，而且隐私泄露也是一个问题。

于是我回去使用codex，但是发现，codex的沙箱机制让我不知道它到底干了啥，而且老是在转圈圈没动静，用得很不舒服（其实也可能单纯是我自己已经习惯了Claude code了）。还有很多配置、记忆迁移起来也挺耗精力，所以我就突然萌生了一个想法，能不能把codex的模型反代出来在Claude code中使用。

为啥我会更习惯使用Claude code（或者说是Claude code的优势）可以参考我的另一篇文章的前半部分

>【学习天地】AI期末论文自救指北（claude；claude code；codex；GPT；DeepSeek；AI agent） https://www.cc98.org/topic/6536301 复制本链接到浏览器或者打开【CC98】微信小程序查看~


## 适用群体
1. Claude被封号，已经习惯了Claude code，需要使用顶级大模型
2. ~~喜欢折腾~~

## 解决方案
其实很简单，我想到的东西，大概率都是有前人想到过的，所以只要拿来就用就可以了。

使用[ccswitch](https://github.com/farion1231/cc-switch)这个软件，这个软件可以将Claude code接入几乎所有的大模型

### 步骤1
![[Claude code邪修使用GPT plus（Claude code; gpt; codex; cc switch）-1783691337096.webp]]
添加供应商，选择codex

### 步骤2
![[Claude code邪修使用GPT plus（Claude code; gpt; codex; cc switch）-1783691465022.webp]]
点击里面的登陆ChatGPT账号，需要注意的是，这一步需要在ChatGPT网页端完成一项设置，打开“为Codex启用设备代码授权”

### 步骤3
![[Claude code中使用GPT plus订阅的模型（Claude code; gpt; codex; cc switch）-1783691555920.webp]]
按你自己的喜好映射好模型

### 步骤4
开启ccswitch中的路由，启动刚刚配置好的供应商，然后就可以愉快的在Claude code中使用GPT5.6啦～～～～

## 后记
依旧哀悼我的Claude😭
往日种种。
![[Claude code中使用GPT plus订阅的模型（Claude code; gpt; codex; cc switch）-1783691719356.webp]]