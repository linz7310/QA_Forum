from flask import Flask,session, g
import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
#对于bug快速定位
#寻找静态模板 有一个相对路径
app = Flask(__name__)
app.config.from_object(config)

#创建一个路由喝视图函数的映射
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)


@app.context_processor
def my_context_processor():
    return {"user":g.user}

if __name__ == '__main__':
    app.run()
