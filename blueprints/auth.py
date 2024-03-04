from flask import Blueprint,render_template,request,jsonify,url_for,redirect,session
from exts import mail,db
from flask_mail import Message
import string
import random
from models import EmailCaptchaModel,UserModel
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
#/auth
bp=Blueprint("auth",__name__,url_prefix="/auth")

# /auth/login
@bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form=LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                #flask消息
                return redirect(url_for("auth.login"))
            #日志文件
            if check_password_hash(user.password,password):
                #cookie:不适合存储太多数据，只适合存储少量的数据
                #cookie一般用来存放登陆授权的东西
                #session:服务器解决方案
                #flask中的session，是经过加密后存储在cookie中的
                session["user_id"]=user.id
                return redirect("/")#跳转到首页
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


#GET：从服务器上获取数据
#POST：将客户端数据提交给服务器
@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else :
    #邮箱验证码验证
    #表单验证：flask-wtf:wtforms
        form=RegisterForm(request.form)
        if form.validate():#自动调用函数
            email=form.email.data
            username=form.username.data
            password=form.password.data
            t=generate_password_hash(password)
            #明文密码password=password
            #flask里面已有加密的
            user = UserModel(email=email,username=username,password=t)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)    
            return redirect(url_for("auth.register"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#bp.route:如果没有指定methods参数，默认就是GET请求
#methods=['POST','GET']
@bp.route("/captcha/email")
def get_email_captcha():
    #/captcha/email/<email>
    #/captcha/email?email=xxx@qq.com
    email=request.args.get("email")
    #4/6:数字，数组和字母的组合
    #string.digits*4:0123456789012345678901234567890123456789
    source = string.digits*4
    captcha=random.sample(source,4)#从source里面随机选择4位
    print(captcha)
    captcha="".join(captcha)

    #I/O操作：耗时
    #使用多进程
    message= Message(subject="注册页面",recipients=[email],body=f"您的验证码是{captcha}")
    mail.send(message)

    #验证用户提交的邮箱和验证码是否对应且正确
    #需要在服务器上缓存一份验证码
    #memcached/redis
    #为方便起见，我们使用数据库存储
    email_captcha=EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    #restful api
    #{code:200/400/500,message:"",data={}}
    return jsonify({"code":200,"message":"","data":None})

@bp.route("/mail/test")
def mail_test():
    message= Message(subject="邮箱测试",recipients=["XXXXXXXXX@qq.com"],body="您的验证码是")
    mail.send(message)
    return "邮件发送成功"

