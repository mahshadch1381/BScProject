import subprocess
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the constants
constants = {
    "total_sections": 10,
     "max_retries": 3,
    "max_distance": 150,
    "p_gas_presence": 1,
    "p_structure_stable": 0.96,
    "p_structure_checkable": 0.89,
    "p_explore_success": 0.95,
    "p_gas_detect": 0.97,
    "p_structure_safe": 0.95,
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
simulation_output_file_accuracy = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output1.txt"

# Accuracy storage
accuracies = []

try:
    for run in range(25):  # Run the command 15 times
        prism_command = [
            r"cd", r"prism-4.8.1\bin", "&&",
            r"prism.bat", model_file, properties_file, "-const", param_str,
            "-simpath", "300", simulation_output_file_accuracy
        ]

        subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)

        gas_detected_flag_true = set()

        with open(simulation_output_file_accuracy, 'r') as file:
            lines = file.readlines()

            columns = lines[0].strip().split()
            current_section_idx = columns.index("current_section")
            gas_detected_flag_idx = columns.index("gas_detected_flag")

            for line in lines[1:]:
                fields = line.strip().split()
                current_section = fields[current_section_idx]
                gas_detected_flag = fields[gas_detected_flag_idx] == "true"

                if gas_detected_flag:
                    gas_detected_flag_true.add(current_section)

        # Calculate accuracy
        detected_count = len(gas_detected_flag_true)
        total_sections = constants["total_sections"]
        accuracy = detected_count / total_sections
        accuracies.append(accuracy)
        print(f"Run {run + 1}: Accuracy = {accuracy:.2f}")

    # Calculate and report average accuracy
    average_accuracy = sum(accuracies) / len(accuracies)
    print(len(accuracies))
    print(f"\nAverage Accuracy over 25 runs: {average_accuracy:.2f}")

    # Plot accuracy results
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 26), accuracies, marker='o', label="Accuracy per Run")  # Adjust x-axis range to 25
    plt.axhline(y=average_accuracy, color='r', linestyle='--', label=f"Average Accuracy: {average_accuracy:.2f}")
    plt.title("Accuracy of Gas Detection Over 25 Runs")  # Update title to reflect 25 runs
    plt.xlabel("Run Number")
    plt.ylabel("Accuracy")
    plt.xticks(range(1, 26, 2))  # Optional: Adjust x-axis ticks for readability
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Save plot
    accuracy_plot_file = "plots\plot_s1_accuracy.png"
    plt.savefig(accuracy_plot_file, format='png')
    plt.show()


except subprocess.CalledProcessError as e:
    print("Error during execution:", e)
    print(e.output)
