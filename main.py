from flask import Flask, render_template, request, send_from_directory
import sqlite3
import time

app = Flask(__name__)

global db
db = sqlite3.connect('db/timeline.db', check_same_thread=False)

@app.route('/')
def main():
    cursor = db.cursor()
    cursor.execute('''SELECT DISTINCT chart FROM jobs''')
    chartlist = []
    for row in cursor.fetchall():
        chartlist.append(row)
    return render_template('get.html', chartlist=chartlist)

@app.route('/<chart>', methods=['GET', 'DELETE'])
def timeline(chart):
    joblist = []
    cursor = db.cursor()

    if request.method == 'GET':
        cursor.execute('''SELECT name, start, stop FROM jobs WHERE chart=?''',
            (chart,))
        for row in cursor.fetchall():
            joblist.append(row)
        return render_template('timeline.html', chart=chart, joblist=joblist)
    elif request.method == 'DELETE':
        cursor.execute('''SELECT * FROM jobs''')
        for row in cursor.fetchall():
            joblist.append(row)
        cursor.execute('''DELETE FROM jobs WHERE chart = ?''', (chart,))
        db.commit()
        return 'Deleted ' + chart

@app.route('/<chart>/<job>/<status>', methods=['POST'])
def chart(chart, job, status):
    if request.method == 'POST':
        epoch_milliseconds = int(round(time.time() * 1000))
        cursor = db.cursor()

        if status == 'start':
            print("Adding start value", epoch_milliseconds, "to chart", chart, "and job", job)
            cursor.execute('''INSERT INTO jobs(name, chart, start)
                      VALUES(?,?,?)''', (job, chart, epoch_milliseconds))
        elif status == 'stop':
            cursor.execute('''UPDATE jobs SET stop = ? WHERE chart = ? AND name = ?''',
                (epoch_milliseconds, chart, job))
        db.commit()

        return '200'

if __name__ == "__main__":
    cursor = db.cursor()
    try:
        cursor.execute('''
            CREATE TABLE jobs(id INTEGER PRIMARY KEY, name TEXT, chart TEXT,
                               start TEXT, stop TEXT )
        ''')
    except sqlite3.OperationalError:
        print('Using existing DB')
    db.commit()

    app.run(host='0.0.0.0', debug=False)
