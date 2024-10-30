import os

# Get a list of all installed libraries
installed_packages = os.popen('pip freeze').read().splitlines()

# Loop through each library and uninstall it
for package in installed_packages:
    package_name = package.split('==')[0]  # Extract package name
    os.system(f"pip uninstall -y {package_name}")
