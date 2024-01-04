from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def machine_failure_analysis():
    # Load data from a dataset
    data = pd.read_csv('F:/Python/machinedata.csv')

    # Calculate overall failure rate
    overall_failure_rate = data['failures'].sum() / len(data['failures'])

    # Calculate failure rate per production line
    line_failure_rates = (data.groupby('production_line')['failures'].sum() / 25).to_dict()

    # Identify production lines with high failure rates
    high_failure_lines = [line for line, rate in line_failure_rates.items() if rate >= overall_failure_rate]

    # Determine machine replacement year using replacement theory
    start_year = int(data['start_year'].min())
    machine_replacement_years = {}
    for line in high_failure_lines:
        age = (start_year - 1) % 5  # Age of machine in the last year of the previous 5-year cycle
        cycles = ((2023 - start_year) // 5) + 1  # Number of 5-year cycles between start year and current year
        machine_replacement_years[line] = start_year + (cycles * 5) - age

    # Simulate accuracy (replace this with your actual accuracy calculation)
    accuracy = 1.0

    return render_template('index.html', overall_failure_rate=overall_failure_rate,
                           production_line_data=line_failure_rates, high_failure_lines=high_failure_lines,
                           machine_replacement_years=machine_replacement_years, accuracy=accuracy)

if __name__ == '__main__':
    app.run(debug=True)
