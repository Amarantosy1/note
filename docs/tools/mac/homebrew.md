[homebrew](https://brew.sh/) 是macOS中非常好用的包管理工具，我在[[Macos实用工具]]一文中有提到过，在使用的过程中可能会碰到一些问题，在此记录一下。
```bash
# 下载卡住，原因很大可能是终端里面的代理没配置好，可以使用以下命令
set -e https_proxy
set -e http_proxy

set -x https_proxy http://127.0.0.1: <你的代理端口>
set -x http_proxy http://127.0.0.1: <你的代理端口>
```