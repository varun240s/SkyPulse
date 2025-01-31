import os

def generate_tree(directory, prefix=""):
    tree_structure = []
    entries = sorted(os.listdir(directory), key=lambda x: (os.path.isdir(os.path.join(directory, x)), x.lower()))
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        connector = "└── " if index == entries_count - 1 else "├── "
        tree_structure.append(f"{prefix}{connector}{entry}")

        if os.path.isdir(path):
            extension = "    " if index == entries_count - 1 else "│   "
            tree_structure.extend(generate_tree(path, prefix + extension))

    return tree_structure

def save_tree_to_file(directory, output_file):
    tree_structure = generate_tree(directory)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{os.path.basename(directory)}/\n")
        f.write("\n".join(tree_structure))
    print(f"Directory structure saved to {output_file}")

# Set your project directory path
project_dir = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS"  # Change this if needed
output_file = os.path.join(project_dir, "directory_structure.txt")

# Generate and save the tree structure
save_tree_to_file(project_dir, output_file)
