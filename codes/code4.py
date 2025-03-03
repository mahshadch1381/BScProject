import subprocess
import matplotlib.pyplot as plt

# File paths
MODEL_FILE = r"..\..\first_model.prism"
PROPERTIES_FILE = r"..\..\properties.props"
COST_FILE_PATH =  r"consts\consts4.txt"


# Main logic to read costs and process results
def main():
    result_data = {'group': [], 'property_5': [], 'property_7': []}
    counter_group = 1

    with open(COST_FILE_PATH, 'r') as cost_file:
        for line in cost_file:
            if line.strip():
                cost_group = extract_constants(line)
                process_prism_results(cost_group, counter_group, result_data)
            counter_group += 1

    # Save and plot results
    property_5_file = "plots/plot_results4.png"
    comparison_file = "plots/plot_comparison_result4.png"

    plot_property_5(result_data, property_5_file)
    plot_comparison_with_tables(result_data, comparison_file)

    print(f"Property 5 plot saved to {property_5_file}")
    print(f"Comparison plot saved to {comparison_file}")

# Function to extract constants from a line
def extract_constants(line):
    constants = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            constants[key.strip()] = float(value.strip()) if "." in value else int(value.strip())
    return constants

# Function to run PRISM and process results
def process_prism_results(cost_group, counter_group, result_data):
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])
    prism_command = [
        r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", MODEL_FILE, PROPERTIES_FILE, "-const", param_str
    ]
    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        output = result.stdout
        parse_prism_output(output, cost_group["p_send_success_lead"], counter_group, result_data)
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM for group {counter_group}:\n", e.stderr)

# Function to parse PRISM output
def parse_prism_output(output, p_success, counter_group, result_data):
    property_number = 1
    for line in output.splitlines():
        if "Result" in line:
            print(f"Result for cost group {counter_group}, property {property_number}: {line}")
            if property_number == 5:
                property_5 = float(line.split(":")[1].strip())
                result_data['group'].append(p_success)
                result_data['property_5'].append(property_5)
            elif property_number == 7:
                property_7 = float(line.split(":")[1].strip())
                result_data['property_7'].append(property_7)
            property_number += 1

# Function to plot Property 5 and its table
def plot_property_5(result_data, output_file):
    plt.figure(figsize=(12, 6))

    # Plot Property 5
    plt.subplot(121)
    plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Max reward when "all robots ready" seen')
    plt.xlabel('p_send_success_lead')
    plt.ylabel('Max reward for :F "area_checked" {"all_robots_ready"}')
    plt.title('Probability of Successful Send in Lead vs Max Reward')
    plt.grid(True)
    plt.legend()

    # Table for Property 5
    plt.subplot(122)
    plt.axis('off')
    table_columns = ["p_send_success_lead",  "MaxRewardAllRobotsReady"]
    table_data = list(zip(result_data['group'], result_data['property_5']))
    table = plt.table(cellText=table_data, colLabels=table_columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust the font size here
    plt.title("p_send_success_lead VS Max Reward all_robots_ready")

    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()

# Function to plot comparison between Property 5 and Property 7
def plot_comparison_with_tables(result_data, output_file):
    plt.figure(figsize=(16, 8))

    # Plot comparison
    plt.subplot(121)
    plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Max reward when "all robots ready" seen')
    plt.plot(result_data['group'], result_data['property_7'], marker='s', color='r',  label='Max reward when "section not checkale" seen')
    plt.xlabel('p_send_success_lead')
    plt.ylabel('Max reward ')
    plt.title("Comparison of max reward in different conditions")
    plt.grid(True)
    plt.legend()

    # Combined table for Property 5, Property 7, and Difference
    plt.subplot(122)
    plt.axis('off')

    table_columns = ["p_send_success_lead",  "MaxRewardAllRobotsReady", "MaxRewardNotCheckable", "Difference"]
    table_data = [
        (
            result_data['group'][i],
            result_data['property_5'][i],
            result_data['property_7'][i],
            result_data['property_7'][i] - result_data['property_5'][i]
        )
        for i in range(len(result_data['group']))
    ]

    table = plt.table(
        cellText=table_data,
        colLabels=table_columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size
    table.scale(1.2, 1.4)  # Adjust table scaling
    plt.title("Comparison of max reward in different conditions Table")
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()


if __name__ == "__main__":
    main()
