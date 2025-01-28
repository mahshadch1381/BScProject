import subprocess
import matplotlib.pyplot as plt


# File paths
model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
cost_file_path = r"consts\random_data.txt"


def parse_cost_line(line):
    """Parse a line from the cost file into a dictionary."""
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())
    return param_dict


def build_prism_command(cost_group):
    """Build the PRISM command for execution."""
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])
    return [
        r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]


def process_prism_output(output, cost_group, result_data, counter_group):
    """Process the PRISM output and update the result_data dictionary."""
    total_section = cost_group["total_sections"]
    result_data[0].append(total_section)

    property_number = 1
    for line in output.splitlines():
        if "Result" in line:
            print(f"Result for cost group {counter_group}, property {property_number}: {line}")
            value_str = line.split(":")[1].strip()

            if property_number == 10:
                numerical_value = float(value_str.split()[0].strip())
                result_data[property_number].append(round(numerical_value, 5))
            else:
                if value_str.lower() in ["true", "false"]:
                    result_data[property_number].append(value_str)
                else:
                    numerical_value = float(value_str)
                    result_data[property_number].append(round(numerical_value, 5))

            property_number += 1


def run_prism_with_cost_group(cost_group, counter_group, result_data):
    """Run PRISM with the given cost group and process the results."""
    prism_command = build_prism_command(cost_group)
    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        process_prism_output(result.stdout, cost_group, result_data, counter_group)
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counter_group}:\n", e.stderr)


def generate_result_table(result_data, columns):
    """Generate the result table for visualization."""
    table_data = list(zip(*[result_data[key] for key in range(11)]))

    plt.figure(figsize=(12, 6))
    plt.axis("off")
    plt.title("Result Table for Properties", fontsize=14)

    table = plt.table(
        cellText=table_data,
        colLabels=columns,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.2)

    add_explanations_below_table()


def add_explanations_below_table():
    """Add explanations below the result table."""
    explanation_text = """
    Property 1: From any state, if unsafe area is detected, system in next step will reach unsafe state.
    Property 2: From any state, if safe area is detected, system in next step will reach safe state.
    Property 3: From any state, if low energy is detected, robot will eventually recover.
    Property 4: From any state, proper distance is maintained.
    Property 5: Maximum expected REWARD to reach area_checked state and it has the conditions for the robots to return to the initial state.
    Property 6: Minimum expected REWARD to reach area_checked state and it has the conditions for the robots to return to the initial state. 
    Property 7: Maximum expected REWARD to reach area_checked state and it has the conditions for the section cannot be checked.
    Property 8: Safety condition, all sections should be checked (with probability of 1).
    Property 9: Finally, all robots should be at initialize situation.
    Property 10: Failure condition, when there is failure in connection or low energy for robots.
    """

    plt.text(
        0.01, -0.15, explanation_text, fontsize=7, ha="left", va="top", transform=plt.gca().transAxes
    )


def save_table_as_image(output_file):
    """Save the generated table as an image file."""
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, format="png", bbox_inches="tight")
    plt.show()


def main():
    # Initialize result_data
    result_data = {i: [] for i in range(11)}

    # Read the cost file and process each line
    counter_group = 1
    with open(cost_file_path, 'r') as cost_file:
        for line in cost_file:
            if line.strip():
                cost_group = parse_cost_line(line)
                run_prism_with_cost_group(cost_group, counter_group, result_data)
            counter_group += 1

    # Define column labels
    columns = ["Total Sections"] + [f"Property {i}" for i in range(1, 11)]

    # Generate and save the result table
    generate_result_table(result_data, columns)
    save_table_as_image("plots/result_properties_table_with_explanations.png")


if __name__ == "__main__":
    main()
