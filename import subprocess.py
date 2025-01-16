import subprocess

# Define the PRISM model and properties file paths
model_file = r"C:\Aterm9\Karshensi_Project\first_model.prism"
properties_file = r"C:\Aterm9\Karshensi_Project\properties.props"

# Path to the file that contains the parameter sets
cost_file_path = r"C:\Aterm9\Karshensi_Project\costs.txt"

# Function to parse a line into a dictionary of parameters
def parse_cost_line(line):
    param_dict = {}
    # Strip any extra spaces and split the line into key-value pairs based on commas
    for param in line.strip().split(","):
        # Split each key-value pair by '='
        key_value = param.split("=")
        
        # Ensure that each param has both a key and a value
        if len(key_value) == 2:
            key, value = key_value
            # Handle float and int values
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())  
    return param_dict

# Function to run PRISM with a specific cost group
def run_prism_with_cost_group(cost_group,counterGroup):
    # Construct the parameter string for PRISM constants
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])

    # Define the PRISM command
    prism_command = [
        r"cd", r"C:\Program Files\prism-4.8.1\bin", "&&",  # Change to PRISM bin directory
        r"prism.bat", model_file, properties_file, "-const", param_str  # Execute the PRISM command
    ]

    # Run the PRISM command and capture the output
    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        
        # Capture the output
        output = result.stdout
        propertyNumber=1
        # Split the output into lines and check for lines containing the word "Result"
        for line in output.splitlines():
            if "Result" in line:
                print(f"Result for cost group {counterGroup} , property { propertyNumber} : {line}")
                propertyNumber= propertyNumber+1
                   # Print lines that contain "Result"
    
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)

# Read the cost values from the file and process each one
counterGroup = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():  # Skip empty lines
            cost_group = parse_cost_line(line)  # Parse the line into a parameter dictionary
            run_prism_with_cost_group(cost_group,counterGroup )
        counterGroup = counterGroup+ 1  # Run the PRISM model with the parsed parameters
