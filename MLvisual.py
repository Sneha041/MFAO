import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data from a dataset
data = pd.read_csv('F:/Python/machinedata.csv')

# Calculate overall failure rate
failure_rate = data['failures'].sum() / len(data['failures'])  # assuming 25 days of production per line

# Calculate failure rate per production line
line_failure_rates = data.groupby('production_line')['failures'].sum() / 25

# Visualize failure rate per production line
plt.figure(figsize=(10, 6))
sns.barplot(x=line_failure_rates.index, y=line_failure_rates.values)
plt.title('Failure Rate per Production Line')
plt.xlabel('Production Line')
plt.ylabel('Failure Rate')
plt.xticks(rotation=45)
plt.show()

# Identify production lines with high failure rates
high_failure_lines = line_failure_rates[line_failure_rates >= failure_rate].index.tolist()

# Split the data into features and target
X = data.drop(['production_line', 'failures'], axis=1)
y = data['failures']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on the test set and evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Determine machine replacement year using replacement theory
start_year = int(data['start_year'].min())

replacement_year = {}
for line in high_failure_lines:
    age = (start_year - 1) % 5  # Age of machine in the last year of the previous 5-year cycle
    cycles = ((2023 - start_year) // 5) + 1  # Number of 5-year cycles between start year and current year
    replacement_year[line] = start_year + (cycles * 5) - age

# Print results
print("Overall failure rate:", failure_rate)
print("Failure rate per production line:", line_failure_rates)
print("Production lines with high failure rates:", high_failure_lines)
print("Machine replacement years:", replacement_year)
print("Accuracy:", accuracy)
