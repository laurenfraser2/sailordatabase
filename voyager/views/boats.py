
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape
from flask import redirect
from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")
def _get_boats(conn, query):
        return execute(conn, f"SELECT DISTINCT Boats.name FROM Sailors, Boats, Voyages WHERE Voyages.sid = Sailors.sid and Boats.bid = Voyages.bid and Sailors.name = '{query}'")
def _add_boat(conn,query1, query2):
        return execute(conn, f"INSERT INTO Boats(name, color) VALUES ('{query1}', '{query2}')")

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)

    @bp.route("/boats/sailed-by", methods=["POST", "GET"])
    def _get_boats_sailed():
        with get_db() as conn:
            query = request.form['sailor-name']
            rows = _get_boats(conn, query)
        return render_template("table.html", name = "sailor-name", rows = rows)

    @bp.route("/boats/add", methods=["POST", "GET"])
    def add_boats_():
        with get_db() as conn: 
            if(request.method == "GET"):
                return render_template("/boats.html")
            if(request.method == "POST"):
                query1 = request.form['new-bname']
                query2 = request.form['new-bcolor']
                _add_boat(conn, query1, query2)
                return redirect('/boats')

