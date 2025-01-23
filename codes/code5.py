import subprocess
import matplotlib.pyplot as plt


def get_float_from_string(line):
    property = float(line.split(":")[1].strip())
    return property

def run_command(prism_command):
     result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
     output = result.stdout
     return output

def check_result(line,propertyNumber,result_data,p_explore_success):
     if propertyNumber == 5:
        property_5 = get_float_from_string(line)
        result_data['group'].append(p_explore_success)
        result_data['property_5'].append(property_5)
     elif propertyNumber == 7:
        property_7 = get_float_from_string(line)
        result_data['property_7'].append(property_7)
     return result_data    

def parse_cost_line(line):
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())  
    return param_dict

def prepare_command():
    properties_file = r"C:\Aterm9\Karshensi_Project\all\properties.props"
    model_file = r"C:\Aterm9\Karshensi_Project\all\first_model.prism"
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])
    prism_command = [
        r"cd", r"C:\Program Files\prism-4.8.1\bin", "&&", 
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]
    return prism_command

def run_prism_with_cost_group(cost_group, counterGroup, result_data):
    prism_command = prepare_command()
    try:
        output =run_command(prism_command)
        propertyNumber = 1
        p_explore_success = cost_group["max_retries"]
        for line in output.splitlines():
            if "Result" in line:
                print(f"Result for cost group {counterGroup} , property { propertyNumber} : {line}")
                result_data = check_result(line,propertyNumber,result_data,p_explore_success)
                propertyNumber += 1
    
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)

result_data = {'group': [],'property_5': [],'property_7': []}

cost_file_path = r"C:\Aterm9\Karshensi_Project\all\consts\consts5.txt"
counterGroup = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():  
            cost_group = parse_cost_line(line)
            run_prism_with_cost_group(cost_group, counterGroup, result_data)
        counterGroup += 1 


plt.figure(figsize=(10, 6))

# Plot Property 5
plt.subplot(121)
plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Property 5')
plt.xlabel('max_retries')
plt.ylabel('Max reward for :F "area_checked" {"all_robots_ready"}')
plt.title('maximum number of resends vs max reward')
plt.grid(True)
plt.legend()

# Table for Property 5
plt.subplot(122)
plt.axis('off')
columns = ["max_retries", "max reward"]
data = list(zip(result_data['group'], result_data['property_5']))
plt.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
plt.title("max_retries , max reward")
plt.tight_layout()

output_file = "plots/plot_results5.png" 
plt.savefig(output_file, format='png', dpi=300) 

plt.close()
