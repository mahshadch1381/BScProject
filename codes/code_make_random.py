import random

def generate_data_line():
    total_sections = random.randint(1, 20)
    max_retries = random.randint(1, 12)
    max_distance = random.randint(21, 210)
    p_explore_success = round(random.uniform(0.5, 0.99), 2)
    p_gas_detect = round(random.uniform(0.5, 0.99), 2)
    p_structure_safe = round(random.uniform(0.5, 0.99), 2)
    p_gas_presence =  round(random.uniform(0.5, 0.99), 2)
    p_structure_stable =  round(random.uniform(0.5, 0.99), 2)
    p_structure_checkable =  round(random.uniform(0.5, 0.99), 2)
    p_send_success =  round(random.uniform(0.5, 0.99), 2)
    p_send_success_lead = round(random.uniform(0.5, 0.99), 2)
    min_energy_lead = random.randint(10, 29)
    min_energy_gas_detector = random.randint(10, 29)
    min_energy_safe_detector = random.randint(10, 29)
    min_energy_leader = random.randint(10, 29)
    max_speed_lead = random.randint(21, 180)
    max_speed_gas_detector = random.randint(21, 180)
    max_speed_safe_detector = random.randint(21, 180)
    max_speed_leader = random.randint(21, 180)

    return (f"total_sections={total_sections},max_retries={max_retries},max_distance={max_distance},"
            f"p_explore_success={p_explore_success},p_gas_detect={p_gas_detect},"
            f"p_structure_safe={p_structure_safe},p_gas_presence={p_gas_presence},"
            f"p_structure_stable={p_structure_stable},p_structure_checkable={p_structure_checkable},"
            f"p_send_success={p_send_success},p_send_success_lead={p_send_success_lead},"
            f"min_energy_lead={min_energy_lead},min_energy_gas_detector={min_energy_gas_detector},"
            f"min_energy_safe_detector={min_energy_safe_detector},min_energy_leader={min_energy_leader},"
            f"max_speed_lead={max_speed_lead},max_speed_gas_detector={max_speed_gas_detector},"
            f"max_speed_safe_detector={max_speed_safe_detector},max_speed_leader={max_speed_leader}")

# Generate 10 lines of data and save them to a file
with open("consts/random_data.txt", "w") as file:
    for _ in range(10):
        file.write(generate_data_line() + "\n")

print("Data generated and saved to random_data.txt")
