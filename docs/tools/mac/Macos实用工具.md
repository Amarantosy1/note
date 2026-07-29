---
type: article
discipline: personal
subject: Mac
topic: mac使用技巧
status: permanent
created: 2026-04-13
---
我的主力电脑从Windows换成Mac也已经一年了，去年这个时候收了台二手的M1 8+256体验了一下，发现确实是非常符合我的心意，现在换成M4 24+256啦，也想趁这个时间写一份这一年使用体验。

## 一、我眼中的Mac的优点和缺点
### 优点
- 最大的优点就是续航和重量，我真的很乐意背着Mac book Air去上课/自习/开会，不用专门去找一个有插座的地方。
- 跟苹果全家桶的生态联动很好
- 没有风扇，没有声音（当然也可以是缺点，长时间高负载会降频）
- 屏幕素质非常好
- iCloud keychain非常好用，指纹就可以当很多账号的通行密钥，不用掏出手机打开authenticator或邮箱接验证码
- 3.5mm耳机接口，在换了M4之后我才体验到的（苹果在M2之后的  MacBook Air更新了适配高阻抗耳机的3.5mm接口），如果用hifi耳机，体验会非常好，推力相当于小一千的前端
- Unix-like的系统对开发者非常友好
- 统一内存跑本地大模型比Windows平台成本低很多（当然这也当不了生产力，只能说是如果感兴趣可以玩一玩体验一下


缺点
- 游戏生态不好
- ~~很多传统工科的软件没得用（虽然跟我没啥关系）~~
- finder的体验感极差。远不如Windows的文件资源管理器，甚至不如直接用终端。（可以说Mac一半的槽点都是finder贡献的。。）

~~文社科技科可以无脑入~~


## 二、工具

### 开发向
#### vs code
 好用的IDE，无须多言，伟大。

#### xcode
 苹果的开发工具，很难用。但是可以用它来给自己的iPhone/mac写app玩
 
#### ghostty
很漂亮，性能很好的终端

#### vim
学习成本很高但是用熟练了非常好用的编辑器，可以用vim tutor过一遍简单的功能，然后再看看一下高级的功能，让AI教你如何在实际场景中用上提高效率，用vim的话，开发的时候基本手不用离开键盘，而且在终端编辑文件也很方便（我其实用不习惯nano。。

#### Zed
轻量的IDE，如果只是很简单的项目/学习/临时修改一下，可以使用Zed，vscode插件装多了之后会启动速度没那么快。

#### 可以搭配一些现代化终端工具：
- zoxide 代替 cd，eza代替ls，fd代替find，tldr代替man，rg代替grep等等（还可以把这些写入Claude.md/Agents.md等vibe coding文件里，让AI使用现代化终端工具代替传统终端工具，提高coding的效率）；
- lazygit可以可视化管理git；
- yazi相当于终端里的文件资源管理体（跟vim的操作逻辑一样，如果熟悉vim甚至可以用这个代替finder）
- fish，比zsh轻量快速，开箱即用，内置语法高亮、历史补全，不用像zsh那么麻烦配置（虽然功能没那么全）


### 笔记向
#### obsidian
非常好用的半开源markdown笔记软件。
颠覆了我之前建很多很多文件夹分类笔记的喜欢，改成使用属性和数据库进行分类，搭配dataview插件真的能极大提高分类整理知识点效率，插件库也非常丰富（~~如果没找到想要的功能的话自己用vibe coding搓一个也行~~
至于在笔记仓库之外的markdown文件，一般直接vim了，或者直接在备忘录里面记就行（不是Typora用不起，而是vim更有性价比，如果要实时渲染的话用nvim/vscode也行

### AI相关
#### Claude Desktop
比网页端多了cowork，虽然lz还没整明白这个cowork应该有啥实际的特别有用的场景（推荐这个其实是因为Claude好用）

#### ollama
可以本地部署AI，在需要隐私的场景可以用一下，实际使用肯定体验是不如云端大模型的


### 浏览器
#### Safari
Apple自带浏览器，简洁轻量，如果是8G内存的Mac一般用chrome会非常卡，这时候使用Safari就是一个很好的选择

#### chrome
这个就没必要写推荐理由了。
写一些推荐插件吧：

Claude for chrome
Claude开发的chrome插件，可以总结网页内容，其他使用场景lz也没尝试过

沉浸式翻译
可以调用AI翻译网页，并且不会破坏网页的格式，非常好用，如果嫌它内置的AI不好用/一些高级功能要收费，还可以自己冲一个10块钱的deepseek API接近去，体验非常好。
![[Pasted image 20260412211102.png]]
![[Pasted image 20260412211041.png]]

Infinity
标签页插件，美观，可以多端同步。
![[Pasted image 20260412210453.png]]

Adguard
广告屏蔽
![[Pasted image 20260412211003.png]]

Extension Manager
可以管理安装的插件
![[Pasted image 20260412210933.png]]

B站下载助手
可以下载B站的视频
![[Pasted image 20260412210906.png]]


### 实用工具
homebrew
很好的包管理工具（相当于Windows的winget+scoop），我现在想下载啥一般都是自己homebrew了，不用去网站点点点安装包又手动安装再删掉，一条命令直接解决，更新和删除也很方便。
lz提到的软件/工具基本上都可以直接用homebrew装
![[Pasted image 20260412211207.png]]

itsycal
一个状态栏显示日历的工具，搭配Apple Calendar很好用
![[Pasted image 20260412191113.png]]

boringNotch
开源刘海屏美化工具，把Mac的刘海变成灵动岛，刘海屏必备。可以管理音乐播放、查看日历、当成文件中转站。
![[Pasted image 20260412211255.png]]
![[Pasted image 20260412211309.png]]

ice
状态栏图表管理工具，适配刘海屏的状态栏管理，可以新开一栏隐藏图标。不过如果是macOS26.4的话，需要到GitHub下载最新的release才不会有bug
![[Pasted image 20260412211346.png]]

keka
开源解压工具
![[Pasted image 20260412211453.png]]

mos
外接鼠标必备
![[Pasted image 20260412211523.png]]

stats
开源监视工具，后台占用低
![[Pasted image 20260412191658.png]]
![[Pasted image 20260412191741.png]]

Mouseboost
增强finder内右键功能，极大程度改善finder的体验
![[Pasted image 20260412211620.png]]

raycast
聚焦搜索的替代，熟练了基本手不用离开键盘。可以保存剪贴板历史、快速打开应用和文件、快速查看日历和提醒事项、快速切换焦点、快速记笔记等等

snipaste
截图工具，可能有更好用的，但lz之前Windows用的是这个，就延续下来了

v2rayN
比clash自定义程度高的梯子客户端，适合折腾自建科学上网节点

Windows App
微软开发的远程桌面，可以局域网连接Windows电脑远程桌面

Inputleap
如果你跟我一样有一台Windows台式机，那就可以使用这个软件，用台式机的外设同时操作Windows和mac


### 其他
Apple Music
大学生6块钱一个月订阅，~~可以弥补网易云听不了周杰伦或其他一些需要付费购买的专辑~~
音质非常好




## 三、实用技巧

触控板
 Mac的触控板确实比Windows笔记本的触控板体验都要好很多，手势操作非常符合逻辑（建议设置一下轻点，这样单击就不用按下去，省力。）

菜单栏
lz对Mac的菜单栏情有独钟，应用的很多操作基本都集成到了菜单栏上，菜单栏可以有很多menubar显示信息

