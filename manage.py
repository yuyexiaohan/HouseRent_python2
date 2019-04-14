# coding=utf-8 
# Time : 2019/1/7
# Author : achjiang


# 从ihome中的init中导入工厂模式创建app
from ihome import create_app, db
# 导入创建脚本的工具
from flask_script import Manager
# 导入数据库迁移工具
from flask_migrate import Migrate,  MigrateCommand


# 创建app实例
app = create_app("develop")

# 创建管理对象
manager = Manager(app)

# 迁移数据库
# 将数据库添加都Migrate对象
Migrate(app, db)

# 设置指令，db--MigrateCommand
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
	# 主程序
	# app.run()
	print '程序开始运行...'
	manager.run()
	print '程序结束运行...'
