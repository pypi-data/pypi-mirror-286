import toml

# Read requirements.txt
with open('requirements.txt', 'r') as req_file:
    requirements = req_file.readlines()

# Load existing pyproject.toml
with open('pyproject.toml', 'r') as toml_file:
    pyproject = toml.load(toml_file)

# Ensure the dependencies section exists
if 'tool' not in pyproject:
    pyproject['tool'] = {}
if 'poetry' not in pyproject['tool']:
    pyproject['tool']['poetry'] = {}
if 'dependencies' not in pyproject['tool']['poetry']:
    pyproject['tool']['poetry']['dependencies'] = {}

# Add Python version if not present
if 'python' not in pyproject['tool']['poetry']['dependencies']:
    pyproject['tool']['poetry']['dependencies']['python'] = "^3.8"  # Adjust the version as needed

# Add dependencies from requirements.txt
for req in requirements:
    req = req.strip()
    if req and not req.startswith('#'):
        # Handle version specifiers if present
        if '==' in req:
            package, version = req.split('==')
        elif '>=' in req:
            package, version = req.split('>=')
        elif '<=' in req:
            package, version = req.split('<=')
        elif '>' in req:
            package, version = req.split('>')
        elif '<' in req:
            package, version = req.split('<')
        else:
            package, version = req, "*"
        
        pyproject['tool']['poetry']['dependencies'][package] = version

# Write updated pyproject.toml
with open('pyproject.toml', 'w') as toml_file:
    toml.dump(pyproject, toml_file)

print("Dependencies from requirements.txt have been added to pyproject.toml")
