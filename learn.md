## 创建项目
django-admin startproject <project_name>
## 新建应用
1. python manage.py startapp <app_name>
2. settings.py中注册app，`INSTALLED_APPS`中添加`PersonLog.apps.PersonlogConfig`,对应修改
3. 创建urls.py进行对应修改

## 部署应用
1. `python manage.py makemigrations` 建立django与数据库的链接代码
2. `python manage.py migrate` 初始化数据库

## 坑
1. Django的`ImageField`没有自带删除与修改时删除原有文件的功能，需要自己添加
2. 使用Django的form校验数据时会把没有输入的键补全，值会默认为空，导致修改时置没有的数据为空

