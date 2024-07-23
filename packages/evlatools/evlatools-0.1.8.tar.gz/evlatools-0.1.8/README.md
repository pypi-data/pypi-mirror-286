

## 打包上传到pypi
```shell
# 创建项目
poetry new evlatools

# 配置pypi的Token
poetry config pypi-token.pypi <token>

# 构建项目
poetry build

# 推送项目到Pypi
poetry publish --build

```


### Poetry常用命令
```shell
# 初始化一个项目，如果不加-n就会询问你项目名和版本之类的
poetry init -n 

#在当前目录建立虚拟环境
poetry init -C . 

# 向 pyproject.toml 添加新的依赖项。等同 pip install flask
poetry add <package>

# 项目打包，然后配合 poetry publish 发布到远程存储库
poetry build 

# 检查当前项目的依赖和环境是否存在问题,每次打包前都要使用一下该指令
poetry check

# 安装项目依赖
poetry install 

# 更新所有依赖到最新版本
poetry update

# 更新指定依赖到最新版本
poetry update <package>

# 锁定依赖版本
poetry lock

# 运行项目，如：poetry run python3 main.py
poetry run 

```


