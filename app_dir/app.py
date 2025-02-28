from flask import Flask, render_template, request, redirect, url_for
import os
from typing import Optional, List, Any
from database import get_db_connection

app = Flask(__name__)

# Set database path relative to this file
db_path = os.path.join(os.path.dirname(__file__), "permits.db")  # Changed to permits.db
print(f"Database path: {db_path}")  # Debug print
app.config["DATABASE"] = db_path


@app.route("/", methods=["GET", "POST"])
def home() -> Any:
    if request.method == "POST":
        name = request.form["name"]
        lot = request.form["lot"]
        price = request.form["price"]
        school = request.form["school"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO permits (name, lot, price, school) VALUES (?, ?, ?, ?)",
            (name, lot, price, school),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("home.html")


@app.route("/permits")
def permits() -> Any:
    try:
        school: Optional[str] = request.args.get("school")
        max_price: Optional[str] = request.args.get("max_price")

        conn = get_db_connection()
        query = "SELECT * FROM permits"
        params: List[Any] = []

        if school or max_price:
            clauses: List[str] = []
            if school:
                clauses.append("school = ?")
                params.append(school)
            if max_price:
                clauses.append("price <= ?")
                params.append(float(max_price))

            query += " WHERE " + " AND ".join(clauses)

        print(f"Executing query: {query} with params: {params}")  # Debug print
        permits_data = conn.execute(query, params).fetchall()
        print(f"Found {len(permits_data)} permits")  # Debug print
        conn.close()
        return render_template("permits.html", permits=permits_data)
    except Exception as e:
        print(f"Error in permits route: {e}")  # Debug print
        return f"Database error: {e}", 500


@app.route("/checkout/<int:permit_id>")
def checkout(permit_id: int) -> Any:
    conn = get_db_connection()
    permit = conn.execute("SELECT * FROM permits WHERE id = ?", (permit_id,)).fetchone()
    conn.close()
    if permit is None:
        return "Permit not found!"
    return render_template("checkout.html", permit=permit)


@app.route("/school_info")
def school_info() -> Any:
    return render_template("school_info.html")


if __name__ == "__main__":
    app.run(debug=True)
