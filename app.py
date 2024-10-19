from flask import Flask, render_template, request, g, redirect, send_file
import sqlite3
import datetime

import io
server = Flask(__name__)

superusers = [1]

def main():
    board(endpoint="/b", name="/b/ Random and Memes", bname="b")
    board(endpoint="/beg", name="/beg/ Backend General", bname="beg")
    board(endpoint="/feg", name="/feg/ Frontend General", bname="feg")
    board(endpoint="/hwg", name="/hwg/ Hardware General", bname="hwg")
    board(endpoint="/csg", name="/csg/ CyberSecurity General", bname="csg")
    server.run(debug=True)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("cschan.db")
        g.db.row_factory = sqlite3.Row
    return g.db

@server.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@server.route("/file/<int:post_id>")
def get_file(post_id):
    db = get_db().cursor()
    post = db.execute("SELECT file FROM posts WHERE id = ?", (post_id,)).fetchone()

    if post and post["file"]:
        return send_file(
            io.BytesIO(post["file"]),
            mimetype="application/octet-stream",
            as_attachment=False,
            download_name="file_from_post"
        )
    else:
        return "File not found", 404

@server.route("/filereply/<int:reply_id>")
def get_reply_file(reply_id):
    db = get_db().cursor()
    post = db.execute("SELECT file FROM replies WHERE id = ?", (reply_id,)).fetchone()

    if post and post["file"]:
        return send_file(
            io.BytesIO(post["file"]),
            mimetype="application/octet-stream",
            as_attachment=False,
            download_name="file_from_post"
        )
    else:
        return "File not found", 404



with server.app_context():
    db = get_db().cursor()
    db.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        file BLOB,
        board TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ip TEXT NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        banned INTEGER NOT NULL,
        postsid TEXT
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS replies (
        ip TEXT NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER,
        opid TEXT NOT NULL,
        content TEXT NOT NULL,
        file BLOB
    )
    ''')

@server.route("/")
def homepage():
    return render_template("index.html")

def board(endpoint, name, bname):
    @server.route(endpoint, methods=["GET", "POST"], endpoint=f"board_{bname}")
    def board_view():
        db = get_db().cursor()
        if request.method == "POST":
            if "submit_npost" in request.form:
                title = request.form.get("posttitle")
                content = request.form.get("postcontent")
                file = request.files["postfile"]
                current_time = datetime.datetime.now()
                date = current_time.strftime("%Y-%m-%d %H:%M")
                ip = request.remote_addr

                try:
                    userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip,))
                    userid = userid_query.fetchone()

                    if not userid:
                        db.execute("INSERT INTO users (ip) VALUES (?)", (ip,))
                        userid = db.lastrowid
                    else:
                        userid = userid[0]

                    file_data = file.read() if file else None

                    db.execute("INSERT INTO posts (title, content, file, userid, board, time) VALUES (?, ?, ?, ?, ?, ?)",
                           (title, content, file_data, userid, bname, date))
                    db.connection.commit()

                except Exception as e:
                    print(f"DB Error: {e}")
                    return "DB Error", 500

            elif "submit_rpost" in request.form:
                opid = request.form.get("opid")
                content = request.form.get("replycontent")
                file = request.files["replyfile"]
                ip = request.remote_addr

                try:
                    userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip,))
                    userid = userid_query.fetchone()

                    if not userid:
                        db.execute("INSERT INTO users (ip) VALUES (?)", (ip,))
                        userid = db.lastrowid
                    else:
                        userid = userid[0]
                except Exception as e:
                    print(f"DB Error: {e}")
                    return "DB Error", 500

                file_data = file.read() if file else None


                db.execute("INSERT INTO replies (ip, opid, content, file, userid) VALUES (?, ?, ?, ?, ?)",
                       (ip, opid, content, file_data, userid))
                db.connection.commit()

            elif "deletebtn" in request.form:
                opid = request.form.get("opid")
                ip = request.remote_addr

                try:
                    userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip,))
                    userid = userid_query.fetchone()

                    if not userid:
                        db.execute("INSERT INTO users (ip) VALUES (?)", (ip,))
                        userid = db.lastrowid
                    else:
                        userid = userid[0]
                except Exception as e:
                    print(f"DB Error: {e}")
                    return "DB Error", 500

                if userid in superusers:
                    db.execute("DELETE FROM posts WHERE id = ?", (int(opid), ))
                db.connection.commit()

            elif "rdeletebtn" in request.form:
                opid = request.form.get("opid")
                ip = request.remote_addr

                try:
                    userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip,))
                    userid = userid_query.fetchone()

                    if not userid:
                        db.execute("INSERT INTO users (ip) VALUES (?)", (ip,))
                        userid = db.lastrowid
                    else:
                        userid = userid[0]
                except Exception as e:
                    print(f"DB Error: {e}")
                    return "DB Error", 500

                if userid in superusers:
                    db.execute("DELETE FROM replies WHERE id = ?", (int(opid), ))
                db.connection.commit()

            elif "submit_banuser" in request.form:
                opid = request.form.get("opid")
                ip = request.remote_addr

                try:
                    userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip,))
                    userid = userid_query.fetchone()

                    if not userid:
                        db.execute("INSERT INTO users (ip) VALUES (?)", (ip,))
                        userid = db.lastrowid
                    else:
                        userid = userid[0]
                except Exception as e:
                    print(f"DB Error: {e}")
                    return "DB Error", 500

                if userid in superusers:
                    db.execute("UPDATE users SET banned = 1 WHERE id = ?", (int(opid), ))

                db.connection.commit()

            elif "submit_unbanuser" in request.form:
                opid = request.form.get("opid")
                ip = request.remote_addr

                try:
                    userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip,))
                    userid = userid_query.fetchone()

                    if not userid:
                        db.execute("INSERT INTO users (ip) VALUES (?)", (ip,))
                        userid = db.lastrowid
                    else:
                        userid = userid[0]
                except Exception as e:
                    print(f"DB Error: {e}")
                    return "DB Error", 500

                if userid in superusers:
                    db.execute("UPDATE users SET banned = 0 WHERE id = ?", (int(opid), ))

                db.connection.commit()

            return redirect(endpoint)



        else:
            posts = db.execute("SELECT * FROM posts WHERE board = ?", (bname, )).fetchall()
            replies = db.execute("SELECT * FROM replies").fetchall()

            ip = request.remote_addr
            userid_query = db.execute("SELECT id FROM users WHERE ip = ?", (ip, ))
            userid = userid_query.fetchone()

            banned_query = db.execute("SELECT banned FROM users WHERE ip = ?", (ip, ))
            banned = banned_query.fetchone()


            return render_template("board.html", title=name, posts=posts, replies=replies, action=endpoint, userid=userid[0], int=int, superusers=superusers, banned=banned[0], board=bname)


@server.route("/ban", methods=["GET"])
def banned_users():
    db = get_db().cursor()
    users = db.execute("SELECT * FROM users WHERE banned = 1").fetchall()
    return render_template("banned.html", users=users)

@server.route("/all", methods=["GET"])
def all_posts():
    db = get_db().cursor()
    posts = db.execute("SELECT * FROM posts").fetchall()
    replies = db.execute("SELECT * FROM replies").fetchall()

    return render_template("all.html", title="All boards", posts=posts, replies=replies, int=int)


if __name__ == "__main__":
    main()
