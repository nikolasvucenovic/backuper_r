import nuke
import shutil
import os
import re

# Find all selected nodes with a file knob
selected_nodes = nuke.selectedNodes()
file_nodes = [n for n in selected_nodes if n.knob('file')]

# Ask user for destination folder path
destination_folder = nuke.getInput('Enter destination folder path')

# Check if destination folder exists
while not os.path.exists(destination_folder):
    destination_folder = nuke.getInput('Enter destination folder path that exists')

# Count the total number of files to be copied
total_files = 0
for node in file_nodes:
    file_path = node.knob('file').value()
    file_dir = os.path.dirname(file_path)
    total_files += len([f for f in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, f))])

# Create a progress task
progress_task = nuke.ProgressTask('Copying files')

# Loop through all file nodes and copy the files to the destination folder
progress = 0
for node in file_nodes:
    # Get the file path from the file knob
    file_path = node.knob('file').value()
    
    rastavljeno = file_path.split('/')
    print(rastavljeno)
    
    # Get the directory of the file path
    file_dir = os.path.dirname(file_path)
    print(file_dir)
    # Get the parent directory of the file directory
    parent_dir = os.path.dirname(file_dir)
    print(parent_dir)
    # Create a new folder in the destination folder for the current file directory
    folder_name = os.path.basename(file_dir)
    print(folder_name)
    print(rastavljeno[-2])
    print(rastavljeno[-3])
    print(rastavljeno[-4])
    print(rastavljeno[-5])
    destination_file_folder4 = os.path.join(destination_folder, rastavljeno[-5])
    destination_file_folder3 = os.path.join(destination_folder, rastavljeno[-5],rastavljeno[-4])
    destination_file_folder2 = os.path.join(destination_folder, rastavljeno[-5],rastavljeno[-4],rastavljeno[-3])
    destination_file_folder = os.path.join(destination_folder, rastavljeno[-5],rastavljeno[-4],rastavljeno[-3],rastavljeno[-2])
    print(destination_file_folder)
    if not os.path.exists(destination_file_folder4):
        os.makedirs(destination_file_folder4)
        print("created levele -3")
    if not os.path.exists(destination_file_folder3) and os.path.exists(destination_file_folder4):
        os.makedirs(destination_file_folder3)
        print("created levele -2")
    if not os.path.exists(destination_file_folder2) and os.path.exists(destination_file_folder3) and os.path.exists(destination_file_folder4):
        os.makedirs(destination_file_folder2)
        print("created levele -1")
    if not os.path.exists(destination_file_folder) and os.path.exists(destination_file_folder2) and os.path.exists(destination_file_folder3) and os.path.exists(destination_file_folder4):
        os.makedirs(destination_file_folder)
        print(destination_file_folder)
        print("created level 1")
    
    # Loop through all files in the directory and copy them to the destination folder
    for filename in os.listdir(file_dir):
        src_file_path = os.path.join(file_dir, filename)
        if os.path.isfile(src_file_path):
            dst_file_path = os.path.join(destination_file_folder, filename)
            
            # Check for a cancel signal
            if progress_task.isCancelled():
                nuke.message('Copying has been cancelled.')
                break
    
            if not os.path.exists(dst_file_path):
                shutil.copy2(src_file_path, dst_file_path)
                print('Copied', src_file_path, 'to', dst_file_path)
            else:
                print('Skipping', src_file_path, '- destination file already exists')

    
        # Update the progress task
        progress += 1
        progress_task.setProgress(int(float(progress)/total_files*100))
        progress_task.setMessage('Copying file {} of {}: {}'.format(progress, total_files, filename))

    # Change the file path in the file knob to the new destination file path
    print(file_path)
    file_name_fromNode = os.path.basename(file_path)
    print(file_name_fromNode)
    dst_file_path_fromNode = os.path.join(destination_file_folder, file_name_fromNode)
    match = re.search(r'\.\d+\.', dst_file_path_fromNode)

    if match:
        # Get the frame number
        frame_number = match.group(0)[1:-1]
        # Get the number of digits in the frame number
        num_digits = len(frame_number)
        # Replace the frame number with a counter with the same number of digits
        counterBasic = chr(35) * num_digits
        counter = "."+counterBasic+"."
        print(counter)
        dst_file_path_with_counter = re.sub(r'\.\d+\.', counter, dst_file_path_fromNode)
        print(dst_file_path_with_counter)
        node.knob('file').setValue(dst_file_path_with_counter.replace('\\', '/'))
    else:
        print(dst_file_path_fromNode)
        node.knob('file').setValue(dst_file_path_fromNode.replace('\\', '/'))
    
    
    print('Changed file path in knob:', node.name() + '.' + node.knob('file').name())

    # Change the color of the node to pure red to indicate that it has been fully copied
    if not progress_task.isCancelled():
        node['tile_color'].setValue(4278190335)
        print('Node', node.name(), 'has been fully copied')

    if progress_task.isCancelled():
        break

# Display a message when all copying is completed
if not progress_task.isCancelled():
    nuke.message('All files have been copied to ' + destination_folder + '\n\nCopying is finished.')
