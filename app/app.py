import os
import psycopg2
from flask import Flask, request

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )


@app.route("/")
def home():
    return """
    <h1>My Homelab Application</h1>
    <p>Flask + Nginx + PostgreSQL</p>
    <p><a href="/database">Test Database</a></p>
    <p><a href="/devices">View Devices</a></p>
    """

@app.route("/devices/add", methods=["GET", "POST"])
def add_device():
    if request.method == "POST":
        name = request.form["name"]
        ip_address = request.form["ip_address"]
        device_type = request.form["device_type"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO devices (name, ip_address, device_type)
            VALUES (%s, %s, %s)
            """,
            (name, ip_address, device_type)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Device added successfully! <a href='/devices'>View Devices</a>"

    return """
    <h1>Add Homelab Device</h1>

    <form method="POST">

        <label>Device Name:</label><br>
        <input type="text" name="name" required>
        <br><br>

        <label>IP Address:</label><br>
        <input type="text" name="ip_address">
        <br><br>

        <label>Device Type:</label><br>
        <input type="text" name="device_type">
        <br><br>

        <button type="submit">Add Device</button>

    </form>

    <br>
    <a href="/devices">Back to Devices</a>
    """

@app.route("/devices/delete/<int:device_id>", methods=["POST"])
def delete_device(device_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM devices WHERE id = %s",
        (device_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return "Device deleted successfully! <a href='/devices'>View Devices</a>"

@app.route("/database")
def database():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return f"""
        <h1>Database Connection Successful</h1>
        <p>{result[0]}</p>
        """

    except Exception as e:
        return f"""
        <h1>Database Connection Failed</h1>
        <p>{e}</p>
        """, 500


@app.route("/devices")
def devices():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, ip_address, device_type, created_at
        FROM devices
        ORDER BY id;
    """)

    devices = cursor.fetchall()

    cursor.close()
    connection.close()

    html = """
    <h1>Homelab Devices</h1>

    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>IP Address</th>
            <th>Type</th>
            <th>Created</th>
            <th>Actions</th>
        </tr>
    """

    for device in devices:
        html += f"""
        <tr>
            <td>{device[0]}</td>
            <td>{device[1]}</td>
            <td>{device[2]}</td>
            <td>{device[3]}</td>
            <td>{device[4]}</td>
            <td>
        	<form method="POST" action="/devices/delete/{device[0]}"
                    onsubmit="return confirm('Are you sure you want to delete this device?');">
                    <button type="submit">Delete</button>
                </form>
            </td>
        </tr>
        """

    html += "</table>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
