Git 版本管理工具实践报告

一、学习资料来源
1. Git 官方文档：https://git-scm.com/doc
2. 菜鸟教程 Git：https://www.runoob.com/git/git-tutorial.html
3. Gitee 官方帮助文档：https://gitee.com/help

二、实践流程
1. 安装 Git：从官网下载安装包，完成安装
2. 配置 Git：设置用户名和邮箱
3. 创建本地仓库：使用 git init 初始化
4. 创建远程仓库：在 Gitee 上创建公开仓库
5. 本地关联远程仓库：git remote add origin 仓库地址
6. 多次提交并推送：完成3次commit + push

三、提交记录说明
1. 第一次提交：创建README.md，记录实践内容
2. 第二次提交：添加练习代码文件，测试版本管理
3. 第三次提交：添加读书笔记，完成任务拓展

四、遇到的问题及解决方法

问题1：git push 时报错，提示权限拒绝
原因：未登录或账号密码错误
解决方法：
1. 使用Gitee的个人令牌登录
2. 重新配置git用户信息
3. 使用 git remote set-url 重新关联仓库

问题2：git push 提示仓库不一致
原因：远程仓库有README，本地没有
解决方法：
1. 先拉取合并：git pull origin main --allow-unrelated-histories
2. 再执行推送：git push origin main

问题3：文件提交不上
解决方法：使用 git add . 提交所有文件，再commit

五、Git 学习心得
通过本次实践，我掌握了Git的基本使用方法，理解了版本控制的意义。
Git可以有效管理代码历史、方便多人协作、避免文件丢失和版本混乱。
未来在项目开发中，我会使用Git进行工程化管理，提升开发效率。
