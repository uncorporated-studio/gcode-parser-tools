import os

# Define the input and output file paths
input_file = 'drawing (6).gcode'
output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}-from-percentage.gcode"

def execute_from_percentage(input_file, output_file, start_percentage):
    # Read all lines from the input file
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()
    
    # Calculate the starting line based on the percentage, ensuring at least the first 4 lines are kept
    total_lines = len(lines)
    start_line = int(total_lines * (start_percentage / 100))

    # If calculated start line is within the first 4 lines, begin from line 5 onward
    if start_line < 4:
        start_line = 4

    # Print the calculated starting line for reference
    print(f"Starting from line {start_line} of {total_lines} (at {start_percentage}% after first 4 lines)")

    with open(output_file, 'w') as f_out:
        # Always write the first 4 lines
        f_out.writelines(lines[:4])
        
        # Then write from the calculated start line to the end
        for line in lines[start_line:]:
            f_out.write(line)

# Specify the starting percentage
start_percentage = 50  # Change this to your desired starting percentage

# Execute the function to write from the calculated line based on the percentage
execute_from_percentage(input_file, output_file, start_percentage)
