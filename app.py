from datetime import date
import re

import pandas as pd
import streamlit as st

from database import add_patient, delete_patient, get_all_patients, init_db, update_patient
from predictor import generate_health_remark


EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def validate_patient(full_name, dob, email, glucose, haemoglobin, cholesterol):
    errors = []

    if not full_name.strip():
        errors.append("Full name is required.")

    if dob > date.today():
        errors.append("Date of birth cannot be a future date.")

    if not re.match(EMAIL_PATTERN, email):
        errors.append("Please enter a valid email address.")

    for label, value in [
        ("Glucose", glucose),
        ("Haemoglobin", haemoglobin),
        ("Cholesterol", cholesterol),
    ]:
        if value < 0:
            errors.append(f"{label} cannot be negative.")

    return errors


def patient_form(button_text, existing_patient=None):
    patient = existing_patient or {}

    full_name = st.text_input("Full Name", value=patient.get("full_name", ""))
    dob = st.date_input(
        "Date of Birth",
        value=patient.get("date_of_birth", date(2000, 1, 1)),
        max_value=date.today(),
    )
    email = st.text_input("Email Address", value=patient.get("email", ""))
    glucose = st.number_input("Glucose", min_value=0.0, value=float(patient.get("glucose", 90.0)))
    haemoglobin = st.number_input("Haemoglobin", min_value=0.0, value=float(patient.get("haemoglobin", 13.0)))
    cholesterol = st.number_input("Cholesterol", min_value=0.0, value=float(patient.get("cholesterol", 180.0)))

    submitted = st.form_submit_button(button_text)

    if not submitted:
        return None

    errors = validate_patient(full_name, dob, email, glucose, haemoglobin, cholesterol)
    if errors:
        for error in errors:
            st.error(error)
        return None

    remark = generate_health_remark(glucose, haemoglobin, cholesterol)

    return {
        "full_name": full_name.strip(),
        "date_of_birth": dob.isoformat(),
        "email": email.strip(),
        "glucose": glucose,
        "haemoglobin": haemoglobin,
        "cholesterol": cholesterol,
        "remarks": remark,
    }


def show_patient_table(patients):
    if not patients:
        st.info("No patient records yet. Add your first patient from the Add Patient page.")
        return

    st.dataframe(pd.DataFrame(patients), use_container_width=True, hide_index=True)


def main():
    st.set_page_config(page_title="Health Prediction App")
    init_db()

    st.title("Health Prediction Application")
    st.write("Store patient blood test records and generate simple health risk remarks.")

    menu = st.sidebar.radio(
        "Menu",
        ["Add Patient", "View Patients", "Update Patient", "Delete Patient"],
    )

    patients = get_all_patients()

    if menu == "Add Patient":
        st.header("Add Patient")
        with st.form("add_patient_form"):
            new_patient = patient_form("Save Patient")

        if new_patient:
            add_patient(new_patient)
            st.success("Patient saved successfully.")
            st.info(f"AI Remark: {new_patient['remarks']}")

    elif menu == "View Patients":
        st.header("All Patients")
        show_patient_table(patients)

    elif menu == "Update Patient":
        st.header("Update Patient")

        if not patients:
            st.info("No patients available to update.")
            return

        patient_options = {f"{patient['id']} - {patient['full_name']}": patient for patient in patients}
        selected_label = st.selectbox("Choose patient", list(patient_options.keys()))
        selected_patient = patient_options[selected_label]
        selected_patient["date_of_birth"] = date.fromisoformat(selected_patient["date_of_birth"])

        with st.form("update_patient_form"):
            updated_patient = patient_form("Update Patient", selected_patient)

        if updated_patient:
            update_patient(selected_patient["id"], updated_patient)
            st.success("Patient updated successfully.")
            st.info(f"New AI Remark: {updated_patient['remarks']}")

    elif menu == "Delete Patient":
        st.header("Delete Patient")

        if not patients:
            st.info("No patients available to delete.")
            return

        patient_options = {f"{patient['id']} - {patient['full_name']}": patient for patient in patients}
        selected_label = st.selectbox("Choose patient to delete", list(patient_options.keys()))
        selected_patient = patient_options[selected_label]

        st.warning(f"You are about to delete {selected_patient['full_name']}.")

        if st.button("Delete Patient"):
            delete_patient(selected_patient["id"])
            st.success("Patient deleted successfully.")


if __name__ == "__main__":
    main()
