from collections import namedtuple

from flask import render_template
from flask import request
from flask import redirect

from voyager.db import get_db, execute

def voyages(conn):
    return execute(conn, f"SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages as v")
def _add_voyage(conn, query1, query2, query3): 
    return execute(conn, f"INSERT INTO Voyages(sid, bid, date_of_voyage) VALUES('{query1}', '{query2}', '{query3}')")

def views(bp):
    @bp.route("/voyages")
    def _voyages():
        with get_db() as conn:
            rows = voyages(conn)
        return render_template("table.html", name="voyages", rows=rows)
    @bp.route("/voyages/add", methods=["POST", "GET"])
    def add_voyages_():
        with get_db() as conn: 
            if(request.method == "GET"):
                return render_template("/voyages.html")
            if(request.method == "POST"):
                query1 = request.form['new-vsid']
                query2 = request.form['new-vbid']
                query3 = request.form['new-vdate']
                _add_voyage(conn, query1, query2, query3)
                return redirect('/voyages')
