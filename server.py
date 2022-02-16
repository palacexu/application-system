import flask
from flask import url_for
import os
# 引入正则表达式对用户输入进行限制
import re
import pymysql

# 初始化
app = flask.Flask(__name__)
# 连接本地mysql数据库
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1518',
                     database='excecise1', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()
# 存储登录用户的名字用户其它网页的显示
users = []


@app.route("/", methods=["GET", "POST"])
def login():
    # 增加会话保护机制(未登录前login的session值为空)
    flask.session['login'] = ''
    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        # 利用正则表达式进行输入判断
        result_user = re.search(r"^[a-zA-Z]+$", user)  # 限制用户名为全字母
        result_pwd = re.search(r"^[a-zA-Z\d]+$", pwd)  # 限制密码为字母和数字的组合
        if result_user != None and result_pwd != None:  # 验证通过
            msg = '用户名或密码错误'
            # 正则验证通过后与数据库中数据进行比较
            sql = "select * from admins where admin_name='" + \
                   user + "' and admin_password='" + pwd + "';"
            cursor.execute(sql)
            result = cursor.fetchone()
            # 匹配得到结果即管理员数据库中存在此管理员
            if result:
                # 登录成功
                flask.session['login'] = 'OK'
                users.append(user)  # 存储登录成功的用户名用于显示
                return flask.redirect(flask.url_for('data_insert'))
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
        user = ''
    return flask.render_template('login.html', msg=msg, user=user)


@app.route('/data_insert', methods=['GET', "POST"])
def data_insert():
    if flask.session.get("login", "") == '':
        print('用户还没有登录!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登录有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from data "
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的信息
        operationID = flask.request.values.get("operationID", "")
        switchID = flask.request.values.get("switchID", "")
        operatorUser = flask.request.values.get("operatorUser", "")
        userOperation = flask.request.values.get("userOperation", "")
        timeSize = flask.request.values.get("timeSize", "")
        opStatus = flask.request.values.get("opStatus", "")
        print(operationID, switchID, operatorUser,userOperation,timeSize,opStatus)
        # 信息存入数据库
        try:
            sql_1 = "insert into data(operationID, switchID, operatorUser, userOperation,timeSize,opStatus)\
                    values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_1, (operationID, switchID, operatorUser, userOperation, timeSize, opStatus))
            insert_result = "成功存入一条用户操作信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "用户操作信息插入失败"
            print(insert_result)
            pass
        db.commit()
        sql_list = "select * from data"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('data_insert.html', insert_result=insert_result, \
                                 user_info=user_info, results=results)


@app.route('/data_select', methods=['GET', 'POST'])
def data_select():
    if flask.session.get("login", "") == '':
        print('用户还没有登录!即将重定向!')
        return flask.redirect('/')
    query_result = ''
    results = ''
    # 当用户登录有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    sql_list = "select * from data"
    cursor.execute(sql_list)
    results = cursor.fetchall()
    # 获取下拉框的数据
    if flask.request.method == 'POST':
        select = flask.request.form.get('selected_one')
        query = flask.request.values.get('query')
        print(select, query)
        # 判断不同输入对数据表进行不同的处理
        if select == 'operationID':
            try:
                sql = "select * from data where operationID = %s; "
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
        if select == 'switchID':
            try:
                sql = "select * from data where switchID = %s ;"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass

        if select == 'operatorUser':
            try:
                sql = "select * from data where operatorUser = %s;"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass

        if select == "userOperation":
            try:
                sql = "select * from data where userOperation = %s;"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
        if select == "timeSize":
            try:
                sql = "select * from data where timeSize = %s;"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
        if select == "opStatus":
            try:
                sql = "select * from data where opStatus = %s;"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
    return flask.render_template(\
         'data_select.html', query_result=query_result, user_info=user_info, results=results)


@app.route('/administrator', methods=['GET', "POST"])
def administrator():
    if flask.session.get("login", "") == '':
        # 用户没有登录
        print('用户还没有登录!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from admins"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    # 当用户登录有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    if flask.request.method == 'POST':
        # 获取输入的管理员信息以及通过正则表达式检测输入合法性
        admin_name = flask.request.values.get("admin_name", "")
        admin_password = flask.request.values.get("admin_password", "")
        admin_name_result = re.search(r"^[a-zA-Z]+$", admin_name)  # 限制用户名为全字母
        admin_password_result = re.search(r"^[a-zA-Z\d]+$", admin_password)  # 限制密码为字母和数字的组合
        # 验证通过
        if admin_name_result != None and admin_password_result != None:  # 验证通过
            # 获取下拉框的数据
            select = flask.request.form.get('selected_one')
            if select == '增加管理员':
                try:
                    sql_1 = "insert into admins(admin_name,admin_password)values(%s,%s)"
                    cursor.execute(sql_1, (admin_name, admin_password))
                    insert_result = "成功增加了一名管理员"
                    print(insert_result)
                except Exception as err:
                    print(err)
                    insert_result = "增加管理员操作失败"
                    print(insert_result)
                    pass
                db.commit()
            if select == '修改管理员密码':
                try:
                    sql = "update admins set admin_password=%swhere admin_name=%s;"
                    cursor.execute(sql, (admin_password, admin_name))
                    insert_result = "管理员" + admin_name + "的密码修改成功!"
                except Exception as err:
                    print(err)
                    insert_result = "修改管理员密码失败!"
                    pass
                db.commit()
            if select == '删除管理员':
                try:
                    sql_delete = "delete from admins where admin_name='" + admin_name + "';"
                    cursor.execute(sql_delete)
                    insert_result = "成功删除管理员" + admin_name
                except Exception as err:
                    print(err)
                    insert_result = "删除管理员失败"
                    pass
                db.commit()
        else:  # 输入验证不通过
            insert_result = "输入的格式不符合要求!"
        # POST方法时显示数据
        sql_list = "select * from admins"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('administrator.html', \
        user_info=user_info, insert_result=insert_result, results=results)


def main():
    # 开启调试功能
    app.debug = True
    # 增加session会话保护,用来对session进行加密)
    app.secret_key = 'jiangxu'
    try:
        # 在本地主机127.0.0.1启动flask服务,默认端口为5000
        app.run()
    # 异常处理
    except Exception as err:
        print(err)
        db.close()  # 关闭数据库连接


if __name__ == '__main__':
    main()
