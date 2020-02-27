from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import redirect

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors as s")
def _get_sailors(conn, query):
        return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors, Boats, Voyages WHERE Voyages.sid = Sailors.sid and Boats.bid = Voyages.bid and Boats.name = '{query}'")
def _add_sailor(conn,query1, query2, query3):
        return execute(conn, f"INSERT INTO Sailors(name, age, experience) VALUES ('{query1}', '{query2}', '{query3}')")
        #return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors, Boats, Voyages WHERE Voyages.sid = Sailors.sid and Boats.bid = Voyages.bid and Boats.name = '{query}'")


def views(bp):

    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)

    @bp.route("/sailors/who-sailed", methods=["POST", "GET"])
    def _get_who_sailed():
        with get_db() as conn:
            query = request.form['boat-name']
            rows = _get_sailors(conn, query)
        return render_template("table.html", name = "boat-name", rows = rows)

    @bp.route("/sailors/add", methods=["POST", "GET"])
    def _add_sailors():
        with get_db() as conn: 
            if(request.method == "GET"):
                return render_template("/sailors.html")
            if(request.method == "POST"):
                query1 = request.form['new-sname']
                query2 = request.form['new-sage']
                query3 = request.form['new-experience']
                _add_sailor(conn, query1, query2, query3)
                return redirect('/sailors')
