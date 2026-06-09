import sqlite3


DB_NAME = "patients.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_patient(patient):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO patients (
            full_name,
            date_of_birth,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient["full_name"],
            patient["date_of_birth"],
            patient["email"],
            patient["glucose"],
            patient["haemoglobin"],
            patient["cholesterol"],
            patient["remarks"],
        ),
    )

    connection.commit()
    connection.close()


def get_all_patients():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    rows = cursor.fetchall()

    connection.close()
    return [dict(row) for row in rows]


def update_patient(patient_id, patient):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE patients
        SET
            full_name = ?,
            date_of_birth = ?,
            email = ?,
            glucose = ?,
            haemoglobin = ?,
            cholesterol = ?,
            remarks = ?
        WHERE id = ?
        """,
        (
            patient["full_name"],
            patient["date_of_birth"],
            patient["email"],
            patient["glucose"],
            patient["haemoglobin"],
            patient["cholesterol"],
            patient["remarks"],
            patient_id,
        ),
    )

    connection.commit()
    connection.close()


def delete_patient(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))

    connection.commit()
    connection.close()
