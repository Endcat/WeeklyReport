## Description

描述遵循以下格式

```yml
路径:
    @调用条件
    路径:
        ...:
            方法:
                - 参数
```

参数视具体情况，要么是query string，要么是form。

以下为API请求体描述

```yml
api:
    login:
        get/post:
            - username
            - password

    logout:
        get:

    @authed
    report:
        get:
        # 获取周报内容，默认为获取自己当前周的周报
        # 如果提供了参数，则会以参数为准
            - author
            - week
        post:
        # 提交周报，非周日调用会返回错误
            - content
    
    @authed
    @is_admin
    admin:
        user:
            get:
            # 目前为获取所有用户的所有信息
            update:
            # 以用户ID为键值更新用户信息
                - id
                - name
                - direction
                - level # 年级
                - token # 密码
                - hidden
                - admin
                - banned
            put:
            # 添加用户
                - name
                - direction
                - level
                ...
                - banned
            delete:
            # 删除id为{id} **且** 密码为{token}的用户
                - id
                - token
        config:
            get:
            # 获取站点设置(起始周，跳过周)
            post:
            # 修改设置
```

关于调用的响应，所有的响应都是以下格式

```jsonc
{
    "result": "success", // 调用成功时为success，否则失败
    "message": "m", // 错误信息
    "data": null // 返回的数据，大部分操作都是null，只有get操作有返回
}
```