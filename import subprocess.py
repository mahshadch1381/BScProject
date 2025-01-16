import subprocess

# Define the PRISM model and properties file paths
model_file = r"C:\Aterm9\Karshensi_Project\first_model.prism"
properties_file = r"C:\Aterm9\Karshensi_Project\properties.props"


constants = {
    "total_sections": 10,
    "max_retries": 3,
    "max_distance": 150,
    "recovery_position": 23,
    "p_explore_success": 0.8,
    "p_gas_detect": 0.7,
    "p_structure_safe": 0.9,
    "p_gas_presence": 0.6,
    "p_structure_stable": 0.8,
    "p_structure_checkable": 0.7,
    "p_send_success": 0.85,
    "p_send_success_lead": 0.9,
    "p_send_success_gas_detector": 0.8,
    "min_energy_lead": 30,
    "min_energy_gas_detector": 25,
    "min_energy_safe_detector": 20,
    "min_energy_leader": 20,
    "max_speed_lead": 125,
    "max_speed_gas_detector": 120,
    "max_speed_safe_detector": 180,
    "max_speed_leader": 122,
}


param_str = ",".join([f"{key}={value}" for key, value in constants.items()])


prism_command = [
    r"cd", r"C:\Program Files\prism-4.8.1\bin", "&&",  # Change to PRISM bin directory
    r"prism.bat", model_file, properties_file, "-const", param_str  # Execute the PRISM command
]

try:
    result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
    
   
    output = result.stdout

   
    for line in output.splitlines():
        if "Result" in line:
            print(line)  

except subprocess.CalledProcessError as e:
    print("Error running PRISM:\n", e.stderr)
