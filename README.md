# SearchLibc python库 说明书


由于原先一直用的 LibcSearcher 最近不太好用了，明明数据库里有，却一直找不到对应的 libc，所以萌发了自己写一个库的想法

功能和原先的 LibcSearcher 差不多，在完成原先功能的基础上并添加了寻找 one_gadget 代码段的功能，当然，ogg 需要安装 one_gadget 软件

ps: 搜索功能参考了该项目【https://github.com/blukat29/search-libc】

# 安装
1. ruby安装
```bash
$ apt install gnupg2 curl
$ curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import -
$ curl -sSL https://get.rvm.io | bash -s stable --rails
如果是root用户，安装完成后记得将"source /usr/local/rvm/scripts/rvm"这句话加入到bashrc中
```

2. one_gadget安装
> gem install one_gadget

3. 库安装
> python setup.py develop

4. libc-database 数据库下载
> 两种办法
> 1) apt-get update & apt-get install -y binutils file wget rpm2cpio cpio zstd jq & ./get all
> 2) 下载了一份存云盘了，可自取 https://mega.nz/file/wU00RQAB#8-w8QSVdudDXGItlNnYGytgWPmgDD4nIS1iHV29VEtg

# 基本使用示例
```python
from SearchLibc import *

#第二个参数，为已泄露的实际地址,或最后12位(比如：d90)，16进制int类型
Libc = SearchLibc("fgets", 0X7ff39014bd90)

system, binsh, atoi = Libc.dump([ 'system', 'str_bin_sh', 'atoi' ])    # 可指定要查找的函数地址
system, binsh = Libc.dump()    # 默认返回system函数以及/bin/sh字符串的地址

ogg = Libc.ogg()    # one_gadget，需要系统内预装one_gadget，安装方法参照以上
```