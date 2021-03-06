OnlineJudgeSys (Tornado Version)
====
运行根目录下gaea.py jserver.py
judger目录下main.py

环境配置说明
-----
        * 开发环境
            Ubuntu 12.04 & 13.04
            python 2.7
            python-dev 2.7
            tornado 3.1
            redis-server 2.6.7
            pymongo 2.5.2
            python-redis 2.4.13
            Lo-runner
        * 开发环境配置
            apt-get python-dev
            tornado python install
            apt-get redis-server python-redis
            pip pymongo
            git Lo-runner python install

09.30 icefish
-----
        * 添加遗漏的lib目录
        * 清除一些无用文件为之后数据库的重构做准备

09.29 icefish
-----
        * 补充之前遗漏的文件
        * 重构整个工程代码结构
            ---root---
                所有的url响应链接放在urls.py
                setting.py存放网站相关settings
            ---lib---
                将一些公共代码统一放在lib目录下,util.py编写项目公共组件
                lib目录下接口将对一些较底层的接口进行封装
            ---models---
                !!!数据库models文件暂时不能用，还需要调整!!!
                将所有数据模型定义为类,存放在models目录下
                (如果一个数据类型需要依赖别的一些子类型,在统一目录下定义)
            ---handlers---
                所有网站响应Handlers目录,一个类型相关的handlers放在对应文件下

09.28 icefish
-----
        * 项目添加log功能,log记录在log目录下judge.log中
        * 代码结构调整,对实现重要函数接口添加注释
        * 因为中文注释的需要,对已经添加注释的文件添加文件编码预处理

07.01 icefish
-----
        * 修正因为单位不统一带来的错误

06.30 icefish
-----
        * 由于底层运行的一些问题,取消了判题服务随服务器启动而启动的功能,改为手动启动
        * user 等待修改
        * 开发预览版本发布

06.29 icefish
-----
        * status 页面支持排序,待实现分页
        * 修复部分因为数据库改动的bug
        * (重要)judge 部分重写,采用开源项目LoRunner 作为沙盒做核心判题服务,实现所有判题结果的判定
        * 根据重构的判题部分修改数据库表结构,修改一些键名,使数据库操作更科学
        * 本地 judge 服务随 tornado 自动开启

        * 待实现
            1.1 判题结束后把代码重新命名放入对应用户目录
            1.2 以往历史,统计等查看

06.28 icefish
-----
        * 修复数据库之间访问由于数据格式错误带来的bug
        * 可以正确响应判题请求,可以接收判题结果并修改相应数据库信息
        * 重要bug修复 开启 judger 的第一次提交判题请求可以立即响应,但结果不能传送的错误
        * 未完成模块
            1.1 Compile Error信息正确显示链接,链接后显示错误信息未完成
            1.2 题目提交信息汇总、用户提交信息汇总未实现

        * 已知问题
            (致命) 2.1 judger 不能正确判断runtime error,独立测试通过
                       错误原因:程序runtime error无法正确接收错误信息,Popen 的returncode中仍返回代码主函数中返回值
                       程序无法正确判断,暂时无解(1.正确接收运行时错误 2.正确得到程序运行时返回值)

06.27 icefish
------
		* 实现测试数据上传
			1.1 在新建题目时,自动在judger/DataFile 下建立对应id的数据文件夹

		* 修改部分数据库模型
		* judger 实现判定 AC,WA,TLE,RE,CE 结果

06.26 icefish
------
		* 实现判题judger模块
			judger 模块设计
			judger 模块完全独立于 tornado 部分，独立服务
			分为本地和网络两个部分
			其中网络部分是为了提供远程判题服务器和集群功能的支持
			本地 judger 服务器默认开启(也是必须)
			judger 识别本地服务，不进行额外的检查工作
			由 redis 提供的同步队列功能，judger 可以自动接受判题请求
			支持阻塞

		* judger 目前现有缺陷
			2.1 只实现本地模块
			2.2 由于暂时没有找到一种较好的内存检测方法，暂不支持内存判断
			2.3 不能保证判题机的安全(不能进行代码安全行检查)
			2.4

		* OJ现有问题
			3.1 admin 添加题目还不能添加数据

06.22 icefish
------
		* 提交题目
			1.1 status数据库集合为 judge_queues
			1.2 提交代码文件名为集合'_id'，放在dissemination目录等待分发
			1.3 提交时记录题目信息、用户提交信息
			1.4 判题请求发送时将设计为异步模式
		* ranklist界面显示
			2.1 仅显示普通用户
		* 部分代码和前台代码调整
		* 部分数据库结构调整
			4.1 pull 后需要执行数据库语句
				ids.remove()
				problems.remove()
				judge_queues.remove()

06.20 icefish
------
bug 修复

06.20 icefish
------
对原有部分代码风格调整
实现基本user
>user密码采用base64库基础加密
>
>user尚未完善
实现前台user响应
实现提交题目form

06.19 icefish
------
		1>套用原前台模板
			1.1 实现主页显示(因为还没有设计user，所以暂不支持登陆)
			1.2 实现题目列表显示
			1.3 实现题目显示

		2>简单实现admin添加题目功能
			2.1 题目id自动增长(id 字段为 '_id')
			2.2 为了实现2.1功能添加 ids collection

06.18 icefish
------
		1>连接数据库到mongoDB
			1.1 数据库为本地数据库 Gaea

		2>采用pymongo

		3>因为mongoDB是Nosql，所以为了统一以后的说法，这里解释一下名词 :)
		    MongoDB 的文档(document),相当于关系数据库中的一行记录
			多个文档组成一个集合(collection),相当于关系数据库的表
			多个集合(collection),逻辑上组织在一起,就是数据库(database)
