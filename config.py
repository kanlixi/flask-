#MySQL所在的主机名，由于是在本主机上运行，因此HOSTNAME为127.0.0.1；
#若在虚拟机或者云服务器上运行，需要把ip地址改为对应虚拟机或云服务器的ip地址
HOSTNAME = '127.0.0.1'

#MySQL监听的端口号，默认3306
PORT = '3306'

#连接MySQL的用户名，读者自己设置
USERNAME = 'root'

#连接MySQL的密码
PASSWORD = '111111'

#MySQL上创建的数据库名称
DATABASE = 'database_learn'

#我们用的数据库驱动程序为pymysql
DB_URI=f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'


SQLALCHEMY_DATABASE_URI=DB_URI


#邮箱配置
MAIL_SERVER='smtp.qq.com'#smtp.163.com
MAIL_USE_SSL=True#加密
MAIL_PORT=465
MAIL_USERNAME="xxxxxxxx@qq.com"#使用自己的qq
MAIL_PASSWORD="xxxxxxxxxxxxxxxxxxxxxx"#开启SMTP服务时生成的授权码
MAIL_DEFAULT_SENDER="xxxxxxxxx@qq.com"#使用自己的qq,与上面qq一致

SECRET_KEY="absddfiurbrqvbunincie"#随便设置，用于加密
