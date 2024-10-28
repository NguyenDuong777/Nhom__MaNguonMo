import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt

# Global variables to store the models and results
scaler = StandardScaler()

models = {'KNN': neighbors.KNeighborsRegressor(n_neighbors=3, p=2), 'Linear Regression': LinearRegression(),
  'Decision Tree': DecisionTreeRegressor(), 'SVM (Linear Kernel)': SVR(kernel='linear'),
  'SVM (RBF Kernel)': SVR(kernel='rbf', C=1.0, epsilon=0.1)}

results = {}


def choose_csv_and_predict():
  global results  # Ensure results is treated as global
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
    y = np.array(df.iloc[:200, 5]).astype(np.float64)  # Labels (column 6 - actual performance)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Get selected model name
    selected_model_name = selected_algorithm.get()
    model = models[selected_model_name]

    # Fit the model and predict, with scaling for SVM
    if 'SVM' in selected_model_name:
      X_train_scaled = scaler.fit_transform(X_train)
      X_test_scaled = scaler.transform(X_test)
      model.fit(X_train_scaled, y_train)
      y_predict = model.predict(X_test_scaled)
    else:
      model.fit(X_train, y_train)
      y_predict = model.predict(X_test)

    # Calculate errors
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)

    # Store the results for comparison
    results[selected_model_name] = {'MSE': mse, 'MAE': mae, 'RMSE': rmse}

    # Plot performance for the selected algorithm
    plot_individual_performance(selected_model_name, y_test, y_predict)

    # Save results to a CSV file
    save_results_to_csv(results)

    # Display the error metrics in a messagebox for the selected algorithm
    messagebox.showinfo("Prediction Result", f"{selected_model_name} - MSE: {results[selected_model_name]['MSE']:.2f}\n"
                                             f"MAE: {results[selected_model_name]['MAE']:.2f}\n"
                                             f"RMSE: {results[selected_model_name]['RMSE']:.2f}")

  except ValueError as ve:
    messagebox.showerror("Error", f"Lỗi giá trị: {ve}")
  except Exception as e:
    messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")


def plot_individual_performance(algorithm_name, y_test, y_predict):
  plt.figure(figsize=(8, 5))
  plt.scatter(y_test, y_predict, color='blue', label='Predicted vs Actual')
  plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linewidth=2,
           label='Perfect Prediction')
  plt.title(f'Performance of {algorithm_name}')
  plt.xlabel('Actual Values')
  plt.ylabel('Predicted Values')
  plt.legend()
  plt.grid()
  plt.tight_layout()
  plt.show()


def save_results_to_csv(results):
  results_df = pd.DataFrame(results).T
  results_df.to_csv('results_comparison.csv', index=True)


def compare_algorithms():
  if not results:
    messagebox.showerror("Error", "Không có kết quả để so sánh.")
    return
  plot_comparison(results)


def plot_comparison(results):
  algorithms = list(results.keys())
  mse_values = [results[algo]['MSE'] for algo in algorithms]
  mae_values = [results[algo]['MAE'] for algo in algorithms]
  rmse_values = [results[algo]['RMSE'] for algo in algorithms]

  x = np.arange(len(algorithms))  # the label locations

  # Plotting the errors
  plt.figure(figsize=(12, 6))
  plt.bar(x - 0.2, mse_values, 0.2, label='MSE')
  plt.bar(x, mae_values, 0.2, label='MAE')
  plt.bar(x + 0.2, rmse_values, 0.2, label='RMSE')

  # Add some text for labels, title and custom x-axis tick labels, etc.
  plt.ylabel('Error Values')
  plt.title('Comparison of Error Metrics for Different Algorithms')
  plt.xticks(x, algorithms)
  plt.legend()

  plt.tight_layout()
  plt.show()


def input_new_data():
  if not results:  # Check if results are available
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

      # Predict using the selected model
      selected_model_name = selected_algorithm.get()
      model = models[selected_model_name]

      if 'SVM' in selected_model_name:
        input_features_scaled = scaler.transform(input_features)
        pi_predicted = model.predict(input_features_scaled)[0]
      else:
        pi_predicted = model.predict(input_features)[0]

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
root.geometry("400x300")

# Create the StringVar for selected algorithm
selected_algorithm = tk.StringVar(value='KNN')  # Default algorithm

# Description label
tk.Label(root, text="Chọn thuật toán:", font=("Arial", 12)).pack(pady=10)

# Algorithm selection dropdown menu
algorithm_menu = tk.OptionMenu(root, selected_algorithm, *models.keys())
algorithm_menu.pack(pady=5)

# Button to select CSV file and predict performance
csv_button = tk.Button(root, text="Chọn file CSV và Dự đoán", command=choose_csv_and_predict)
csv_button.pack(pady=5)

# Button to compare algorithms
compare_button = tk.Button(root, text="So sánh Thuật toán", command=compare_algorithms)
compare_button.pack(pady=5)

# Button to input new data and make predictions
input_button = tk.Button(root, text="Nhập Dữ liệu Mới", command=input_new_data)
input_button.pack(pady=5)

# Button to exit the application
exit_button = tk.Button(root, text="Thoát", command=exit_application)
exit_button.pack(pady=5)

# Run the main loop
root.mainloop()
