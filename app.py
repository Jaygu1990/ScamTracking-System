from flask import Flask, render_template, request
import sqlite3
from difflib import SequenceMatcher

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# String similarity function
def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Form page to add data to the database
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        tiktok_username = request.form["tiktok_username"]
        address = request.form["address"]
        city = request.form["city"]
        province_or_state = request.form["province_or_state"]
        note = request.form["note"]
        reporting_streamer = request.form["reporting_streamer"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (tiktok_username, address, city, province_or_state, note, reporting_streamer) VALUES (?, ?, ?, ?, ?, ?)",
            (tiktok_username, address, city, province_or_state, note, reporting_streamer)
        )
        conn.commit()
        conn.close()

    return render_template("form.html")

@app.route("/query", methods=["GET", "POST"])
def query():
    results = []
    page = int(request.args.get('page', 1))  # Get current page, default to 1
    per_page = 20  # Limit results to 20 per page
    offset = (page - 1) * per_page  # Calculate the offset for pagination

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch current page data
    cur.execute("SELECT * FROM users LIMIT ? OFFSET ?", (per_page, offset))
    rows = cur.fetchall()

    # Check if there are more rows for the next page
    cur.execute("SELECT COUNT(*) FROM users")
    total_rows = cur.fetchone()[0]
    has_next_page = (page * per_page) < total_rows  # Check if next page exists

    if request.method == "POST":
        tiktok_username = request.form.get("tiktok_username", "").strip()
        address = request.form.get("address", "").strip()
        city = request.form.get("city", "").strip()
        province_or_state = request.form.get("province_or_state", "").strip()

        # Filter results based on form input
        if tiktok_username:
            results = [r for r in rows if r["tiktok_username"].lower() == tiktok_username.lower()]
        elif address:
            input_combo = address.lower()
            for row in rows:
                db_combo = row["address"].lower()  # Assuming 'address' is in column 2
                similarity = string_similarity(input_combo, db_combo)
                if similarity >= 0.7:
                    results.append(row)
        else:
            results = rows
    else:
        # If no form submitted (GET request), fetch all data
        results = rows

    cur.close()
    conn.close()

    return render_template("query.html", results=results, page=page, has_next_page=has_next_page)

if __name__ == "__main__":
    app.run(debug=True)


