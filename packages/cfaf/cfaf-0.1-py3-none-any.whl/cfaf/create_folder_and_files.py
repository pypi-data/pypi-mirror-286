import os
import sys

def create_folder_and_files(folder_name):
    if not folder_name:
        print("Usage: cfaf <folder_name>")
        sys.exit(1)

    # Create the main folder
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Folder '{folder_name}' created successfully.")
    except Exception as e:
        print(f"Error creating folder '{folder_name}': {e}")
        sys.exit(1)

    # Define the path for the 'services' directory
    services_folder = os.path.join(folder_name, 'services')

    # Create the 'services' folder
    try:
        os.makedirs(services_folder, exist_ok=True)
        print(f"Folder '{services_folder}' created successfully.")
    except Exception as e:
        print(f"Error creating folder '{services_folder}': {e}")
        sys.exit(1)

    # List of files to create in the 'services' folder
    files = [
        "models.py",
        "schemas.py",
        "routes.py",
        "exceptions.py",
        "enums.py",
        "__init__.py"
    ]
    
    # Create each file in the 'services' directory
    for file_name in files:
        file_path = os.path.join(services_folder, file_name)
        try:
            with open(file_path, 'w') as file:
                pass  # Create an empty file
            print(f"File '{file_path}' created successfully.")
        except Exception as e:
            print(f"Error creating file '{file_path}': {e}")
            sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: cfaf <folder_name>")
        sys.exit(1)

    folder_name = sys.argv[1]
    create_folder_and_files(folder_name)

if __name__ == "__main__":
    main()
