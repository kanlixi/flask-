from flask import Flask,session,g
#g表示global
import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app=Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate=Migrate(app,db)

#blueprint：用来做模块化的
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

#flask db init:只需要执行一次
#flask db migrate:将ORM模型生成迁移脚本
#flask db upgrade:将迁移脚本映射到数据库中

#钩子函数
#before_request/before_first_request/after_request
#hook
@app.before_request
def my_before_request():
   user_id = session.get("user_id")#解密自带的
   if user_id:
      user = UserModel.query.get(user_id)
      setattr(g,"user",user)
   
   else:
      setattr(g,"user",None)
 

#上下文处理器
#上下文处理器的概念：上下文处理器将所有的变量都存储在上下文当中，
#当其他模板需要渲染变量的时候就直接使用上下文处理器中的变量，
#而不需要重新去一个一个去获取
@app.context_processor
def my_context_processor():
   return {"user":g.user}











if __name__ == '__main__':
   app.run(debug = True)