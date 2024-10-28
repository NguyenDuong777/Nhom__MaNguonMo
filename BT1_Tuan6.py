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
import os

# Global variables to store the models and results
scaler = StandardScaler()

models = {
    'KNN': neighbors.KNeighborsRegressor(n_neighbors=3, p=2),
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(),
    'SVM (Linear Kernel)': SVR(kernel='linear'),
    'SVM (RBF Kernel)': SVR(kernel='rbf', C=1.0, epsilon=0.1)
}

results = {}

def choose_csv_and_predict():
    global results  # Ensure results is treated as global
    try:
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not csv_file_path:
            return  # Exit if no file is selected

        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Check if CSV has sufficient columns
        if df.shape[1] < 6:
            messagebox.showerror("Error", "CSV file phải có ít nhất 6 cột.")
            return

        # Select sample size
        sample_size = min(200, len(df))  # Choose up to 200 rows if available
        x = np.array(df.iloc[:sample_size, 0:5]).astype(np.float64)
        y = np.array(df.iloc[:sample_size, 5]).astype(np.float64)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        # Get selected model name
        selected_model_name = selected_algorithm.get()
        model = models[selected_model_name]

        # Fit model and predict, with scaling for all models
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        model.fit(X_train_scaled, y_train)
        y_predict = model.predict(X_test_scaled)

        # Calculate errors
        mse = mean_squared_error(y_test, y_predict)
        mae = mean_absolute_error(y_test, y_predict)
        rmse = np.sqrt(mse)

        # Store results
        results[selected_model_name] = {'MSE': mse, 'MAE': mae, 'RMSE': rmse}

        # Plot individual performance
        plot_individual_performance(selected_model_name, y_test, y_predict)

        # Save results to CSV
        save_results_to_csv(results)

        # Show metrics
        messagebox.showinfo("Prediction Result", f"{selected_model_name} - MSE: {mse:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}")

    except ValueError as ve:
        messagebox.showerror("Error", f"Lỗi giá trị: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

def plot_individual_performance(algorithm_name, y_test, y_predict):
    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, y_predict, color='blue', label='Predicted vs Actual')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linewidth=2, label='Perfect Prediction')
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

    x = np.arange(len(algorithms))  # Label locations
    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.2, mse_values, 0.2, label='MSE')
    plt.bar(x, mae_values, 0.2, label='MAE')
    plt.bar(x + 0.2, rmse_values, 0.2, label='RMSE')

    plt.ylabel('Error Values')
    plt.title('Comparison of Error Metrics for Different Algorithms')
    plt.xticks(x, algorithms)
    plt.legend()
    plt.tight_layout()
    plt.show()

def input_new_data():
    if not results:
        messagebox.showerror("Error", "Vui lòng chọn file CSV và thực hiện dự đoán trước.")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Nhập Dữ liệu Mới")
    labels = ["HS (Hours Studied)", "PS (Previous Scores)", "EA (Extracurricular Activities)", "SH (Sleep Hours)", "SQP (Sample Question Papers Practiced)", "PI (Performance Index)"]
    entries = []

    for idx, text in enumerate(labels):
        tk.Label(input_window, text=text).grid(row=idx, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(input_window)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries.append(entry)

    def predict_and_compare():
        try:
            input_features = np.array([float(entry.get()) for entry in entries[:5]]).reshape(1, -1)
            pi_actual = entries[5].get()

            # Scale the input features
            input_features_scaled = scaler.transform(input_features)
            selected_model_name = selected_algorithm.get()
            model = models[selected_model_name]
            pi_predicted = model.predict(input_features_scaled)[0]

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

            messagebox.showinfo("Prediction Result", result_message)

        except ValueError:
            messagebox.showerror("Error", "Vui lòng nhập tất cả các giá trị số hợp lệ.")
        except Exception as e:
            messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

    predict_btn = tk.Button(input_window, text="Predict", command=predict_and_compare)
    predict_btn.grid(row=6, column=0, columnspan=2, pady=10)
    exit_btn = tk.Button(input_window, text="Thoát", command=input_window.destroy)
    exit_btn.grid(row=7, column=0, columnspan=2, pady=5)

def exit_application():
    root.destroy()

# Create main GUI window
root = tk.Tk()
root.title("Student Performance Predictor")
root.geometry("400x300")

# Create the StringVar for selected algorithm
selected_algorithm = tk.StringVar(value='KNN')

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
