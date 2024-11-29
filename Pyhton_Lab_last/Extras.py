import pandas as pd
import matplotlib.pyplot as plt

# Simulated dataset (acts as input)
default_data = pd.DataFrame({
    "Subject": ["Math", "Science", "English", "History", "Geography"],
    "Marks": [85, 90, 75, 88, 92]
})

# Simulate reading from a file (this dataset will be used as input)
file_path = "CSE_data.csv"  # Simulated file name
try:
    # Simulate file reading: Replace this line with actual `pd.read_csv(file_path)` if a real file exists
    print("Simulating file reading...")
    data = default_data  # Replace this line with `pd.read_csv(file_path)` if using real data
    print("Data loaded successfully. Data preview:")
    print(data.head())
except FileNotFoundError:
    # Use a sample dataset if file is missing
    print("File not found. Using sample dataset.")
    data = default_data

# Ensure the data has the required columns
if 'Subject' in data.columns and 'Marks' in data.columns:
    # Plotting a bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(data['Subject'], data['Marks'], color='skyblue')
    plt.title("Marks by Subject")
    plt.xlabel("Subjects")
    plt.ylabel("Marks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("The dataset does not contain the required 'Subject' and 'Marks' columns.")
