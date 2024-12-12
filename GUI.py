import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score

# Database connection and data preprocessing
conn = psycopg2.connect(
    dbname="credit_scoring",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5432"
)

query_application = "SELECT * FROM application_record;"
query_credit = "SELECT * FROM credit_record;"

data_application = pd.read_sql_query(query_application, conn)
data_credit = pd.read_sql_query(query_credit, conn)

conn.close()


def preprocess_application_data(data):
    label_encoders = {}
    for col in ['code_gender', 'flag_own_car', 'flag_own_realty', 'name_income_type',
                'name_education_type', 'name_family_status', 'name_housing_type', 'occupation_type']:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    data.fillna(0, inplace=True)

    return data, label_encoders


def preprocess_credit_data(data):
    status_mapping = {'C': 0, 'X': 0, '0': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6}
    data['status'] = data['status'].map(status_mapping)
    data.fillna(0, inplace=True)
    return data


data_application, label_encoders = preprocess_application_data(data_application)
data_credit = preprocess_credit_data(data_credit)

data = pd.merge(data_application, data_credit, on='id', how='inner').fillna(0)

X = data.drop(columns=['id', 'status'])
y = data['status'] > 2

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

# GUI Design
def check_loan_approval():
    try:
        user_id = int(user_id_entry.get())
        loan_amount = float(loan_amount_entry.get())
        user_data = data[data['id'] == user_id]

        if user_data.empty:
            messagebox.showerror("Error", "User ID not found.")
            return

        salary = user_data.iloc[0, 5]

        if loan_amount > 3 * salary:
            result_label.config(text="Decision: Rejected", fg="red")
            return

        user_features = user_data.drop(columns=['id', 'status'])
        user_features = scaler.transform(user_features)

        prediction = model.predict(user_features)

        if prediction[0] == 0:
            result_label.config(text="Decision: Approved", fg="green")
        else:
            result_label.config(text="Decision: Rejected", fg="red")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs.")


root = tk.Tk()
root.title("Credit Scoring Application")
root.geometry("600x500")
root.configure(bg="#f4f4f4")

title_label = tk.Label(root, text="Credit Scoring System", font=("Helvetica", 20, "bold"), bg="#f4f4f4", fg="#333")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE)
frame.pack(pady=20, padx=20, fill="both", expand=True)

user_id_label = tk.Label(frame, text="User ID:", font=("Helvetica", 14), bg="#ffffff")
user_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

user_id_entry = tk.Entry(frame, font=("Helvetica", 14))
user_id_entry.grid(row=0, column=1, padx=10, pady=10)

loan_amount_label = tk.Label(frame, text="Loan Amount (KZT):", font=("Helvetica", 14), bg="#ffffff")
loan_amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

loan_amount_entry = tk.Entry(frame, font=("Helvetica", 14))
loan_amount_entry.grid(row=1, column=1, padx=10, pady=10)

check_button = ttk.Button(frame, text="Check Loan Approval", command=check_loan_approval)
check_button.grid(row=2, column=0, columnspan=2, pady=20)

result_label = tk.Label(root, text="Decision: N/A", font=("Helvetica", 16), bg="#f4f4f4", fg="#333")
result_label.pack(pady=10)

root.mainloop()
