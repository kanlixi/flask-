from flask import Blueprint,request,render_template,g,redirect,url_for
from .forms import QuestionForm,AnswerForm
from models import QuestionModel,AnswerModel
from exts import db
from decorators import login_required
#/auth
bp=Blueprint("qa",__name__,url_prefix="/")#设置为首页

#http://127.0.0.1:5000
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html",questions = questions)


@bp.route("/qa/public",methods=["GET","POST"])
@login_required
def public_question():
    #必须先登陆再填写问卷
    #我们使用装饰器实现该功能
    #if not g.user:
    #    return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form=QuestionForm(request.form)
        if form.validate:
            title=form.title.data
            content=form.content.data
            question=QuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            #跳转
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/delete")
def delete_qa():
    #1.查找
    qa=QuestionModel.query.get(3)
    #2.从db.session中删除
    db.session.delete(qa)
    #3.将db.session中的修改，同步到数据库中
    db.session.commit()
    return "数据删除成功！"


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question=QuestionModel.query.get(qa_id)
    return render_template("detail.html",question=question)

@bp.route("/answer/public",methods=["POST"])
#也可以@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content=form.content.data
        question_id=form.question_id.data
        answer=AnswerModel(content=content,question_id=question_id,author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question_id")))

@bp.route("/search")
def search():
    #/search?q=flask
    #/search/<q>
    #post,request.form
    q=request.args.get("q")
    questions=QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html",questions=questions)

#项目包含：
#url传参
#邮件发送
#ajax
#orm与数据库
#jinja2模板
#cookie与session原理
#搜索

#flask全栈开发
#flask实战：flask+vue前后端分离的论坛系统；
#websocket实战


#前端
#部署，例如excel文件上传

