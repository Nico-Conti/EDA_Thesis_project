# Read the content of the binary file
with open('finger_person_stroop_4_E.txt', 'rb') as file:
    content = file.read()

sample_size = 8  # Each sample is 8 bytes
samples_to_change_trigger = 5760  # Number of samples after which trigger becomes 1

# Modify the last 4 bytes of each sample to zero
modified_values = bytearray()
for i in range(0, len(content), sample_size):
    sample = bytearray(content[i:i + sample_size])
    sample[-4:] = b'\x00' * 4  # Set the last 4 bytes to zero
    
    if i // sample_size >= samples_to_change_trigger:
        sample[-4:] = b'\x01\x01\x01\x01'  # Change trigger value to 1
    
    modified_values.extend(sample)

# Write the modified data back to the binary file
with open('modified.txt', 'wb') as modified_file:
    modified_file.write(modified_values)
