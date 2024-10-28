
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt

# Global variables to store the model and data
knn_model = None
X_train_global = None
X_test_global = None
y_train_global = None
y_test_global = None


def choose_csv_and_predict():
  global knn_model, X_train_global, X_test_global, y_train_global, y_test_global
  try:
    # Let user choose CSV file
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not csv_file_path:
      return  # If no file is selected, exit the function

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Check if the CSV has at least 6 columns
    if df.shape[1] < 6:
      messagebox.showerror("Error", "CSV file phải có ít nhất 6 cột.")
      return

    # Assume first 5 columns are features and the 6th column is the actual performance
    x = np.array(df.iloc[:200, 0:5]).astype(np.float64)  # Features (columns 1-5)
    y = np.array(df.iloc[:200, 5:6]).astype(np.float64)  # Labels (column 6 - actual performance)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Create the KNN model
    knn = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
    knn.fit(X_train, y_train)

    # Store the model and data globally
    knn_model = knn
    X_train_global, X_test_global, y_train_global, y_test_global = X_train, X_test, y_train, y_test

    # Predict based on the test set
    y_predict = knn.predict(X_test)

    # Calculate errors
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)

    # Display the error metrics in a messagebox
    messagebox.showinfo("Prediction Result", f"MSE: {mse:.2f}\nMAE: {mae:.2f}\nRMSE: {rmse:.2f}")

    # Plot error graph
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(y_test)), y_test, 'ro-', label='Actual Performance')
    plt.plot(range(len(y_predict)), y_predict, 'bo-', label='Predicted Performance')

    # Plot error lines between predicted and actual values
    for i in range(len(y_test)):
      plt.plot([i, i], [y_test[i], y_predict[i]], 'g--')

    plt.title('Actual vs Predicted Performance')
    plt.xlabel('Student')
    plt.ylabel('Performance')
    plt.legend()
    plt.tight_layout()
    plt.show()

  except Exception as e:
    messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")


def input_new_data():
  if knn_model is None:
    messagebox.showerror("Error", "Vui lòng chọn file CSV và thực hiện dự đoán trước.")
    return

  # Create a new window for data input
  input_window = tk.Toplevel(root)
  input_window.title("Nhập Dữ liệu Mới")

  # Labels and entry boxes for features
  labels = ["HS (Hours Studied)", "PS (Previous Scores)", "EA (Extracurricular Activities)", "SH (Sleep Hours)",
            "SQP (Sample Question Papers Practiced)", "PI (Performance Index)"]
  entries = []

  for idx, text in enumerate(labels):
    tk.Label(input_window, text=text).grid(row=idx, column=0, padx=10, pady=5, sticky='e')
    entry = tk.Entry(input_window)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    entries.append(entry)

  def predict_and_compare():
    try:
      # Get input values
      hs = float(entries[0].get())
      ps = float(entries[1].get())
      ea = float(entries[2].get())
      sh = float(entries[3].get())
      sqp = float(entries[4].get())
      pi_actual = entries[5].get()

      input_features = np.array([hs, ps, ea, sh, sqp]).reshape(1, -1)

      # Predict
      pi_predicted = knn_model.predict(input_features)[0][0]

      if pi_actual:
        pi_actual = float(pi_actual)
        mse = (pi_actual - pi_predicted) ** 2
        mae = abs(pi_actual - pi_predicted)
        rmse = np.sqrt(mse)
        result_message = (f"Predicted PI: {pi_predicted:.2f}\n"
                          f"Actual PI: {pi_actual:.2f}\n"
                          f"MSE: {mse:.2f}\n"
                          f"MAE: {mae:.2f}\n"
                          f"RMSE: {rmse:.2f}")
      else:
        result_message = f"Predicted PI: {pi_predicted:.2f}"

      # Display the result
      messagebox.showinfo("Prediction Result", result_message)

    except ValueError:
      messagebox.showerror("Error", "Vui lòng nhập tất cả các giá trị số hợp lệ.")
    except Exception as e:
      messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

  # Predict button
  predict_btn = tk.Button(input_window, text="Predict", command=predict_and_compare)
  predict_btn.grid(row=6, column=0, columnspan=2, pady=10)

  # Exit button
  exit_btn = tk.Button(input_window, text="Thoát", command=input_window.destroy)
  exit_btn.grid(row=7, column=0, columnspan=2, pady=5)


def exit_application():
  root.destroy()


# Create main GUI window
root = tk.Tk()
root.title("Student Performance Predictor")

# Set window size
root.geometry("400x200")

# Description label
tk.Label(root, text="Chọn chức năng dưới đây:", font=("Arial", 14)).pack(pady=20)

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Button to choose CSV and predict
choose_csv_btn = tk.Button(button_frame, text="Chọn File CSV và Dự đoán", width=25, command=choose_csv_and_predict)
choose_csv_btn.grid(row=0, column=0, padx=10, pady=5)

# Button to input new data
input_data_btn = tk.Button(button_frame, text="Nhập Dữ liệu Mới", width=25, command=input_new_data)
input_data_btn.grid(row=1, column=0, padx=10, pady=5)

# Exit button
exit_btn_main = tk.Button(root, text="Thoát", width=10, command=exit_application)
exit_btn_main.pack(pady=10)

# Start the Tkinter loop
root.mainloop()