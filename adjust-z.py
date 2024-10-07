import os

# Path to your G-code file
input_file = 'test.gcode'
output_file = f'modified-{os.path.splitext(os.path.basename(__file__))[0]}.gcode'

def modify_gcode_with_height(input_file, output_file, steps, decrement):
    # Read all lines from the input file
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()
    
    # Keep the first three lines and the last line
    start_lines = lines[:3]
    end_line = lines[-1]
    
    with open(output_file, 'w') as f_out:
        # Write the first three lines without modification
        f_out.writelines(start_lines)
        
        current_step = 0
        current_z = 0.0  # Starting Z height (adjust as needed)

        # Process only the middle section (4th to second-to-last line) for modification
        for line in lines[3:-1]:
            # Check if the line is a G1 with a Z parameter
            if 'G1' in line and 'Z' in line:
                # Adjust Z height every specified number of steps
                if current_step == steps:
                    current_z -= decrement
                    current_step = 0
                else:
                    current_step += 1

                # Update the Z parameter in the line
                parts = line.split()
                new_parts = []
                
                for part in parts:
                    if part.startswith('Z'):
                        part = f'Z{current_z:.2f}'
                    new_parts.append(part)

                modified_line = ' '.join(new_parts)
                f_out.write(modified_line + '\n')
            else:
                # Write any line as-is if it doesn't match the criteria for modification
                f_out.write(line)

        # Write the last line from the original file without modification
        f_out.write(end_line)

# Parameters for height control
steps = 10  # Number of steps to adjust Z height
decrement = 0.5  # Amount to lower Z each interval

# Run the function to modify G-code with height control and specific line retention
modify_gcode_with_height(input_file, output_file, steps, decrement)
