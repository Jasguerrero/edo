from flask import Flask
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    dbname='edo_db',
    user='user',
    password='password',
    host='db',
    port='5432'
)

@app.route('/')
def hello():
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    cur.close()
    return str(db_version)

if __name__ == "__main__":
    app.run(debug=True)
