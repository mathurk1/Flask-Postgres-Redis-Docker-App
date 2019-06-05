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
    sql_qry = "SELECT * FROM PROD.test_table"
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)