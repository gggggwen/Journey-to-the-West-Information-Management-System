## 哈尔滨工程大学--信息管理系统--课设作业--西游记信息管理系统

### 1.运行

#### 1.1.配置
在 jtw_info_management/settigs.py 中:
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "Journey_to_the_West",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "USER": "用户自拟",
        "PASSWORD": "用户自拟",
    }
}
```
#### 1.2.首次运行运行
```
conda activate info_system # 创建虚拟环境,仅首次使用需要

python initialize_databases.py #初始化数据库,仅首次使用需要

python manage.py runserver # 运行服务器
```
### 2.实现

前端纯HTML 后端Django

### 3.功能亮点
a.可实现显示角色图谱,图谱**可随鼠标**动态滑动,点击角色节点可跳转至相应角色介绍。

![image](https://github.com/gggggwen/Journey-to-the-West-Information-Management-System/blob/main/media/demo/demo.gif)