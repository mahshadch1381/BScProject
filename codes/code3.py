import subprocess
import matplotlib.pyplot as plt


model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
cost_file_path = r"consts\consts3.txt"



def get_parameter(key_value):
    """Parses a key-value string and returns a dictionary entry."""
    key, value = key_value
    return key.strip(), float(value.strip()) if "." in value else int(value.strip())

def plot_comparison(data1, data2, group_label, property_label, title, output_file):
    plt.figure(figsize=(16, 8))
    plt.subplot(121)
    plt.plot(data1['group'], data1['property'], marker='o', color='b', label='Property 5')
    plt.plot(data2['group'], data2['property'], marker='x', color='r', label='Property 7')
    plt.xlabel(group_label)
    plt.ylabel(property_label)
    plt.title(f"{title} (Graph)")
    plt.grid(True)
    plt.legend()
    table_data = [( data1['group'][i],  # p_gas_detect 
            data1['property'][i],  # Reward for Property 5
            data2['property'][i],  # Reward for Property 7
            data2['property'][i] - data1['property'][i]  # Difference
            )  for i in range(len(data1['group']))
    ]
    plt.subplot(122)
    plt.axis('off')
    columns = [group_label, "Reward (Property 5)", "Reward (Property 7)", "Difference"]
    table = plt.table(
        cellText=table_data,
        colLabels=columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size
    table.scale(1.2, 1.4)  # Adjust table scaling
    plt.title("Comparison Table: Property 5 vs Property 7 with Difference")
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()

def check_values_line(line):
    """Parses a line from the cost file into a dictionary."""
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = get_parameter(key_value)
            param_dict[key] = value
    return param_dict



def extract_results_from_output(output, p_gas_detect, result_data, counter_group):
    """Extracts and processes results from PRISM's output."""
    property_number = 1
    for line in output.splitlines():
        if "Result" in line:
            print(f"Result for cost group {counter_group}, property {property_number}: {line}")
            process_property_result(line, property_number, p_gas_detect, result_data)
            property_number += 1



def process_property_result(line, property_number, p_gas_detect, result_data):
    """Processes a single property result and updates the result_data."""
    if property_number == 5:
        property_5 = float(line.split(":")[1].strip())
        result_data['group'].append(p_gas_detect)
        result_data['property_5'].append(property_5)
    elif property_number == 7:
        property_7 = float(line.split(":")[1].strip())
        result_data['property_7'].append(property_7)



def plot_results(result_data, output_file):
    """Generates and saves a plot of the results with a table."""
    plt.figure(figsize=(10, 6))

    # Plot Property 5
    plt.subplot(121)
    plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Property 5')
    plt.xlabel('p_gas_detect')
    plt.ylabel('Max reward for :F "area_checked" {"all_robots_ready"}')
    plt.title('Probability of Success of the Gas Detector vs Max Reward')
    plt.grid(True)
    plt.legend()


    # Table for Property 5
    plt.subplot(122)
    plt.axis('off')
    columns = ["p_gas_detect", "max reward"]
    data = list(zip(result_data['group'], result_data['property_5']))
    plt.table(cellText=data, colLabels=columns, loc='center', cellLoc='center', fontsize=9)
    plt.title("p_gas_detect, Max Reward")
    plt.tight_layout()

    plt.savefig(output_file, format='png', dpi=300)
    plt.close()



def prism_connect_and_run(cost_group, counter_group, result_data):
    """Runs PRISM with the given cost group and processes the results."""
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])
    prism_command = [
         r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]
    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        extract_results_from_output(result.stdout, cost_group["p_gas_detect"], result_data, counter_group)
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counter_group}:\n", e.stderr)



# Main script
result_data = {'group': [],'property_5': [], 'property_7': []}
counter_group = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():
            cost_group =check_values_line(line)
            prism_connect_and_run(cost_group, counter_group, result_data)
        counter_group += 1

data1 = {'group': result_data['group'], 'property': result_data['property_5']}
data2 = {'group': result_data['group'], 'property': result_data['property_7']}
plot_comparison(data1, data2, "p_gas_detect", "Max Reward", "Comparison of Properties 5 and 7", "plots/plot_comparison_result3.png")

# Plot results
output_file = "plots/plot_results3.png"
plot_results(result_data, output_file)

