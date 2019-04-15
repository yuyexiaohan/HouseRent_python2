### flask-ihome项目指导
1. 下载项目文件到指定文件夹。

2. 使用`mkvirtualenv ihome_python2`创建一个项目的虚拟环境，并进入

3. 在虚拟环境中使用`pip install -r requirements.txt`命令安装项目所需要的包

4. 在MySQL数据库中创建项目需要的数据库

5. 在config.py文件中配置数据库等相关参数信息

6. 配置后，对数据库进行表的迁移：
    
     - 使用`python2 manage.py db init`命令初始化，
     - 使用`python2 manage.py db migrate -m 'init tables'`命令初始化表
     - 使用'python manage.py db upgrade'命令升级
     
7. 在该项目的根目录下输入`python manage.py runserver`默认开启`127.0.0.1:5000`端口，或使用命令`python manage.py runserver -h host -p prot`命令指定相关host和port;

8. 根据蓝图及各个url在浏览器中输入地址，类似`host:port/url`进行访问。