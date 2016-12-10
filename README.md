# 为知笔记python-exporter

大部分源码是借助网上github源码,这里由于一些原因没有直接引用原作者地址,当然你可以从源码中看到原始文件的出处.
该程序主要是为了导出所有为知笔记,以便于备份笔记(由于免费帐号过了试用期不再提供同步服务原因)

`开发/测试环境: ubuntu 16.10 python2.7.12+`

我仅仅在linux上面测试过,至于windows 上如果报错,大部分可能会因为文件命名规则.

## 使用

### 下载所有源码

 `git clone https://github.com/yoke88/wiznoteExporter.git`


### 更改test.py
 ```
  wizUsername='YourWiznoteAccountName'
  wizPassword='wiznotePassword'
 ```

 ### 执行test.py
 linux 下直接cd 到wiznoteExporter ,然后执行`./test.py`即可
 windows 下你可能需要先安装python2.7 ,然后步骤同上.
 

