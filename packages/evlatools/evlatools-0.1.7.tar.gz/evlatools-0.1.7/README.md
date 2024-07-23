

## Poetry常用命令
```shell
# 创建项目
poetry new evlatools

# 构建项目
poetry build

# 配置Pypi的Token
poetry config pypi-token.pypi ${Pypi的Token}

# 推送项目到Pypi
poetry publish

# 向 pyproject.toml 添加依赖项，等同 pip install flask
poetry add name


```


### 常用命令样例
poetry init -n 初始化一个项目，如果不加-n就会询问你项目名和版本之类的
poetry init -C . #在当前目录建立
poetry -v 或 -vv 或 -vvv 用法：主要是输出的信息v越多，输出的调试信息越多，有点类似于logger等级
poetry add 向 pyproject.toml 添加新的依赖项。等同 pip install flask
poetry add flask --group=test #添加分组名.名字为test
poetry add flask --dev #添加相当于--group=dev
poetry build 把项目打包。然后配合 poetry publish 发布到远程存储库
poetry check 命令用于检查当前项目的依赖和环境是否存在问题,每次打包前都要使用一下该指令
poetry config 管理配置设置,这个比较关键，详细讲解

poetry update 更新 Poetry 到最新版本。
poetry lock 锁定 Poetry 安装的系统要求。
poetry run 在适当的环境中运行命令，这样就不需要进入虚拟环境中运行程序

