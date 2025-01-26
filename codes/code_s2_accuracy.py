import subprocess
import os
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the constants
constants = {
    "total_sections": 10,
    "max_retries": 3,
    "max_distance": 150,
   
    "p_gas_presence": 0.78,
    "p_structure_stable": 1,
    "p_structure_checkable": 0.89,
    "p_explore_success": 0.7,
    "p_gas_detect": 0.88,
    "p_structure_safe": 0.86,
    "p_send_success": 0.78,
    "p_send_success_lead": 0.86,
  
    "min_energy_lead": 10,
    "min_energy_gas_detector": 10,
    "min_energy_safe_detector": 10,
    "min_energy_leader": 10,
    "max_speed_lead": 120,
    "max_speed_gas_detector": 120,
    "max_speed_safe_detector": 120,
    "max_speed_leader": 120
}

param_str = ",".join([f"{key}={value}" for key, value in constants.items()])

model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"

simulation_output_file_accuracy = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output2_accuracy.txt"

# Store 1 - accuracies
inverted_accuracies = []

try:
    for run in range(25):  # Run the command 25 times
        prism_command = [
            r"cd", r"prism-4.8.1\bin", "&&",
            r"prism.bat", model_file, properties_file, "-const", param_str,
            "-simpath", "300", simulation_output_file_accuracy
        ]

        subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)

        structure_ok_flag_false = set()

        with open(simulation_output_file_accuracy, 'r') as file:
            lines = file.readlines()

            columns = lines[0].strip().split()
            current_section_idx = columns.index("current_section")
            structure_ok_flag_idx = columns.index("structure_ok_flag")

            for line in lines[1:]:
                fields = line.strip().split()
                current_section = fields[current_section_idx]
                structure_ok_flag = fields[structure_ok_flag_idx] == "false"

                if structure_ok_flag:
                    structure_ok_flag_false.add(current_section)

        # Calculate accuracy for structure_ok_flag = false
        false_flag_count = len(structure_ok_flag_false)
        total_sections = constants["total_sections"]
        accuracy = false_flag_count / total_sections

        # Calculate 1 - accuracy
        inverted_accuracy = 1 - accuracy
        inverted_accuracies.append(inverted_accuracy)
        print(f"Run {run + 1}: Accuracy = {inverted_accuracy:.2f}")

    # Calculate and report average 1 - accuracy
    average_inverted_accuracy = sum(inverted_accuracies) / len(inverted_accuracies)
    print(f"\nAverage Accuracy over 25 runs: {average_inverted_accuracy:.2f}")

    # Plot 1 - accuracy results
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 26), inverted_accuracies, marker='o', label="Accuracy per Run")
    plt.axhline(y=average_inverted_accuracy, color='r', linestyle='--', label=f"Average Accuracy: {average_inverted_accuracy:.2f}")
    plt.title(" Accuracy of Structure Stability Check Over 25 Runs")
    plt.xlabel("Run Number")
    plt.ylabel(" Accuracy")
    plt.xticks(range(1, 26, 2))
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Save plot
    accuracy_plot_file = "plots\plot_s2_accuracy.png"
    plt.savefig(accuracy_plot_file, format='png')
    plt.show()

except subprocess.CalledProcessError as e:
    print("Error during execution:", e)
    print(e.output)
