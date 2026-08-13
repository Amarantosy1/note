## 依赖与环境
抽象层无处不在（让别的库来做）
使用虚拟环境
```bash
uv pip install pyproject.toml
```

学会使用uv管理python虚拟环境

## Artifacts & Packaging
在python中，打包一个library为artifact，python中的artifact被称为wheel
```bash
uv build #build wheel
ls dist/ #.whl是wheel，.tar.gz源码压缩包
```

安装软件分为从源码安装和安装预编译二进制文件

## Releases & Versioning
版本号
semantic versioning
补丁版本（1.2.3 - 1.2.4）补丁，完全向后兼容
MINOR（1.2.3 - 1.3.0）添加新功能，向后兼容
MAJOR（1.2.3 - 2.0.0）可能需要破坏性的变更

## Reproducibility
可复现性，大量抽象层中的任意一个有了差异就有可能改变代码的行为。
包管理器的一部分工作是考虑所有依赖项所提供的约束(`uv.lock`)

软件开发的矛盾：新版本会带来破坏，旧版本会出现漏洞

## VMs & Containers
当项目更为复杂，包管理工具不够用的时候，就需要虚拟机了。而更现代的方法是使用容器（Containers），最流行的平台是docker
Docker需要运行在Linux内核，所以在Mac和Windows上，Docker实质是一个轻量级的虚拟机。

## Configuration
A good right-hand rule for thinking about configuration is that the same codebase should be deployable to different environments (development, staging, production) with only configuration changes, never code changes.
配置中的敏感数据一定不能纳入版本控制中

## Services & Orchestration

## Publishing
