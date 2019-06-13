#!/usr/bin/env python3
from flask import Flask
from flask import render_template, request, redirect, url_for
from redis import Redis
from src.database.posgre import get_db_engine

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

db_engine = get_db_engine()

@app.route('/')
def hello():
    redis.incr('hits')
    cnt = redis.get('hits').decode("utf-8")
    return render_template('displayMenu.html', hits=cnt)


@app.route('/dbdisplay')
def db_display():
    sql_qry = "SELECT * FROM PROD.test_table ORDER BY username;"
    result = db_engine.execute(sql_qry)
    return render_template('displayDbData.html', result=result)


@app.route('/dbcapture', methods=['GET', 'POST'])
def db_capture():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        sql_stmt = f'''INSERT INTO PROD.test_table (username, email) 
                       VALUES ('{name}', '{email}')
                    '''
        db_engine.execute(sql_stmt)
        return redirect(url_for('db_display'))
    else:
        return render_template('captureDbData.html')


@app.route('/dbdelete/<name>')
def db_delete(name):
    sql_stmt = f'''DELETE FROM PROD.test_table WHERE username = '{name}';'''
    db_engine.execute(sql_stmt)
    return redirect(url_for('db_display'))


@app.route('/dbupdate/<name>', methods=['GET', 'POST'])
def db_update(name):
    if request.method == 'GET':
        sql_stmt = f'''SELECT * FROM PROD.test_table 
                       WHERE username = '{name}';
                    '''
        result = db_engine.execute(sql_stmt)

        for item in result:
            name = item[0]
            email = item[1]

        return render_template('editDbData.html', name=name, email=email)
    else:
        username = request.form['username']
        email = request.form['email']
        updt_sql_stmt = f'''UPDATE PROD.test_table 
                            SET username = '{username}',
                                email = '{email}'
                            WHERE username = '{name}';'''
        db_engine.execute(updt_sql_stmt)
        return redirect(url_for('db_display'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)