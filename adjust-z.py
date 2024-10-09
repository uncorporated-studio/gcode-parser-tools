import os

# Path to your G-code file
input_file = 'drawing (10).gcode'
output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}-{os.path.splitext(os.path.basename(__file__))[0]}.gcode"

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
        current_travel_z = None  # Initialize to track travel height based on input
        current_drawing_z = 0.0  # Initial drawing height (Z0)

        # Process only the middle section (4th to second-to-last line) for modification
        for line in lines[3:-1]:
            if 'G1' in line and 'Z' in line:
                # Determine whether the Z command is a drawing or travel height
                z_value = None
                for part in line.split():
                    if part.startswith('Z'):
                        z_value = float(part[1:])  # Extract the numerical Z value
                
                # Initialize the current travel height based on the first encountered travel height (if not already done)
                if current_travel_z is None and z_value is not None and z_value > 0:
                    current_travel_z = z_value
                
                # Adjust Z for both travel and drawing moves
                if current_step == steps:
                    current_travel_z -= decrement
                    current_drawing_z -= decrement
                    current_step = 0
                else:
                    current_step += 1

                # Modify the Z value in the line accordingly
                parts = line.split()
                new_parts = []
                
                for part in parts:
                    if part.startswith('Z'):
                        if z_value == 0:  # Drawing height adjustment
                            part = f'Z{current_drawing_z:.2f}'
                        else:  # Travel height adjustment
                            part = f'Z{current_travel_z:.2f}'
                    new_parts.append(part)

                modified_line = ' '.join(new_parts)
                f_out.write(modified_line + '\n')
            else:
                # Write non-Z lines as-is
                f_out.write(line)

        # Write the last line from the original file without modification
        f_out.write(end_line)

# Parameters for height control
steps = 10  # Number of steps to adjust Z height
decrement = 0.02  # Amount to lower Z each interval

# Run the function to modify G-code with consistent Z adjustment
modify_gcode_with_height(input_file, output_file, steps, decrement)
