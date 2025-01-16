import subprocess
import matplotlib.pyplot as plt




model_file = r"C:\Aterm9\Karshensi_Project\first_model.prism"
properties_file = r"C:\Aterm9\Karshensi_Project\properties.props"


cost_file_path = r"C:\Aterm9\Karshensi_Project\costs.txt"


def parse_cost_line(line):
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())  
    return param_dict


def run_prism_with_cost_group(cost_group, counterGroup, result_data):

    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])

    prism_command = [
        r"cd", r"C:\Program Files\prism-4.8.1\bin", "&&", 
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]

    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        
        output = result.stdout
        propertyNumber = 1
        total_section = counterGroup 
        for line in output.splitlines():
            if "Result" in line:
                print(f"Result for cost group {counterGroup} , property { propertyNumber} : {line}")
                if propertyNumber == 5:
                    # Extract property 5 value
                    property_5 = float(line.split(":")[1].strip())
                    result_data['group'].append(total_section)
                    result_data['property_5'].append(property_5)
                elif propertyNumber == 7:
                    # Extract property 7 value
                    property_7 = float(line.split(":")[1].strip())
                    result_data['property_7'].append(property_7)
                elif propertyNumber == 8:
                    # Extract property 8 value
                    property_8 = float(line.split(":")[1].strip())
                    result_data['property_8'].append(property_8)
                
             
                propertyNumber += 1
    
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)

# Initialize data containers for plotting
result_data = {
    'group': [],
    'property_5': [],
    'property_7': [],
    'property_8': []
}


counterGroup = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():  
            cost_group = parse_cost_line(line)
            run_prism_with_cost_group(cost_group, counterGroup, result_data)
        counterGroup += 1 


plt.figure(figsize=(20, 5))


plt.subplot(131)
plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Property 5')
plt.xlabel('Cost Group (Total Section)')
plt.ylabel('Property 5')
plt.title('Cost Group vs Property 5')
plt.grid(True)
plt.legend()


plt.subplot(132)
plt.plot(result_data['group'], result_data['property_7'], marker='o', color='g', label='Property 7')
plt.xlabel('Cost Group (Total Section)')
plt.ylabel('Property 7')
plt.title('Cost Group vs Property 7')
plt.grid(True)
plt.legend()


plt.subplot(133)
plt.plot(result_data['group'], result_data['property_8'], marker='o', color='r', label='Property 8')
plt.xlabel('Cost Group (Total Section)')
plt.ylabel('Property 8')
plt.title('Cost Group vs Property 8')
plt.grid(True)
plt.legend()


plt.tight_layout()
plt.show()
