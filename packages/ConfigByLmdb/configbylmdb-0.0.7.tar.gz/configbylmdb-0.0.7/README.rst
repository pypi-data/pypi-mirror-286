=============
ConfigByLmdb
=============

ConfigByLmdb 是一个基于 lmdb 1.5.1 版本 自定义封装的库，主要用于快速动态读写大量配置信息的数据库工具。

概述
----

lmdb是一个轻量级、本地部署的高性能数据库，ConfigByLmdb 仅对其进行了某些场景简单的接口封装。


安装
----

使用 pip 安装 ConfigByLmdb ：

.. code-block:: bash

    pip install ConfigByLmdb

请注意，由于本项目是 lmdb 的自定义封装版本，可能需要从源代码安装或使用特定的安装步骤。

使用示例
--------

以下是一个简单的使用示例，展示如何使用：

.. code-block:: python

    from ConfigByLmdb import DB,Structure

    db = DB()
    
    db_name = 'db'
    name_db = 'test'

    # 创建或初始化数据库
    print(db.init_db(db_name))

    # 创建命名数据库
    # data = Structure("主键名",[('a',str),('b',str),('c',dict),('d',int),("e",float)]) # 设置数据库结构
    # print(db.create_name_db(db_name,name_db,"这是一个测试命名数据库",data))

    # 添加
    # print(db.write(db_name,name_db,'t1',{'a':"你好",'b':"123",'c':{"f":1,"g":'abc'},"d":189,"e":0.123}))
    # print(db.write(db_name,name_db,'t2',{'a':"hello!",'b':"234",'c':{"f":3,"g":'ret'},"d":49,"e":15.48}))
    # print(db.write(db_name,name_db,'t3',{'a':"A和B",'b':"858",'c':{"f":3,"g":'ret'},"d":49,"e":15.48}))
    # 错误示范(数据格式不对应)
    # l = []
    # for i in range(10):
    #     l.append({'body'+str(i):{'a':"你好",'b':"318",'c':None,"d":4945,"e":185.48}})
    # print(db.batch_write(db_name,name_db,l))
    # 正确示范
    # l = []
    # for i in range(1000):
    #     l.append({'body'+str(i):{'a':"A和B",'b':"315",'c':{"f":3,"g":'ret'},"d":4945,"e":185.48}})
    # print(db.batch_write(db_name,name_db,l))
    # print(db.get_sum(db_name,name_db))

    # 查询
    # print(db.read(db_name,name_db,'body2'))
    # print(db.get(db_name,name_db,['body4','c','f']))
    # 匹配查询
    # print(db.matching(db_name,name_db,"body1",0,10),len(db.matching(db_name,name_db,"body1",0,10)[0]))
    # print(db.matching(db_name,name_db,"修改后的值",0,10),len(db.matching(db_name,name_db,"修改后的值",0,10)[0]))


    # 删除
    # print(db.read(db_name,name_db,'body5'))
    # print(db.remove(db_name,name_db,['body5','c','f']))
    # print(db.read(db_name,name_db,'body5'))
    # print(db.delete(db_name,name_db,'body2'))
    # print(db.read(db_name,name_db,'body2'))

    # 修改
    # print(db.read(db_name,name_db,'body3'))
    # print(db.updata(db_name,name_db,"body3",{'a':"修改后的值",'b':"315",'c':{"t":1},"d":911,"e":1.48}))
    # print(db.read(db_name,name_db,'body3'))
    # print(db.read(db_name,name_db,'body6'))
    # print(db.set(db_name,name_db,['body6','a'],"修改后的值"))
    # print(db.read(db_name,name_db,'body6'))

    # 数据库信息
    # print(db.get_name_database_list(db_name)) # 指定数据库下命名数据库列表
    # print(db.get_db_name_list()) # 所有数据库列表
    # print(db.get_db_info(db_name)) # 数据库配置信息

    # 数据库操作
    # print(db.drop_name_db(db_name,name_db)) # 删除指定命名数据库
    # print(db.get_name_database_list(db_name))
    # print(db.env_close(db_name)) # 关闭指定数据库
    # print(db.cleanup(db_name)) # 删除指定数据库
    # print(db.get_db_name_list())

贡献
----

我们欢迎任何形式的贡献，包括但不限于：

- 报告问题或错误。
- 提供功能请求或改进建议。

许可证
------

本项目采用 OLDAP-2.8 许可证。有关更多信息，请查看 `LICENSE` 文件。
