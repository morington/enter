#!/bin/bash

# Enter: Installation script for Ubuntu

# Colors for console output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print success messages
success() {
  echo -e "${GREEN}$1${NC}"
}

# Function to print error messages
error() {
  echo -e "${RED}$1${NC}"
  exit 1
}

# Check if git is installed
if ! command -v git &> /dev/null; then
  error "Error: git is not installed. Please install git and try again."
fi

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
  error "Error: Python 3 is not installed. Please install Python 3.11 or higher and try again."
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

# Convert version to an integer for comparison (e.g., "3.11" -> 311)
PYTHON_VERSION_NUM=$(echo "$PYTHON_VERSION" | tr -d '.')

# Debug output (optional)
echo "Detected Python version: $PYTHON_VERSION"
echo "Numeric Python version: $PYTHON_VERSION_NUM"

# Check if Python version is 3.11 or higher
if (( 10#$PYTHON_VERSION_NUM < 311 )); then
  error "Error: Python 3.11 or higher is required. Your version: $PYTHON_VERSION"
fi

# Clone the repository from the dev branch
success "Cloning the repository (dev branch)..."
git clone -b dev https://github.com/morington/enter.git || error "Error: Failed to clone the repository."
cd enter || error "Error: Failed to enter the project directory."

# Create a virtual environment
success "Creating a virtual environment..."
python3 -m venv venv || error "Error: Failed to create a virtual environment."

# Activate the virtual environment
source venv/bin/activate || error "Error: Failed to activate the virtual environment."

# Install dependencies
success "Installing dependencies..."
pip install -r requirements.txt || error "Error: Failed to install dependencies."

# Create the config_enter.yml file in the user's home directory
CONFIG_FILE="$HOME/config_enter.yml"
if [[ ! -f "$CONFIG_FILE" ]]; then
  success "Creating an example configuration file in your home directory..."
  cat <<EOL > "$CONFIG_FILE"
scripts:
  gen_ssh_key: |
    if [ ! -f ~/.ssh/id_rsa ]; then
      echo "SSH key not found. Generating a new key..."
      ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -q
      echo "SSH key successfully generated."
    else
      echo "SSH key already exists."
    fi

aliases:
  hello:
    description: "Prints a greeting"
    args:
      name:
        description: "User's name"
        default: "Guest"
    rargs:
      place:
        description: "Place to greet the user"
    commands: |
      echo "Hello, {name}!"
      echo "Welcome to {place}!"

  generate_server_ssh_key:
    description: "Generate an SSH key"
    commands: |
      {gen_ssh_key}
EOL
fi

# Update config.ini to point to the config_enter.yml file
CONFIG_INI="src/config.ini"
success "Updating config.ini to point to the new configuration file..."
cat <<EOL > "$CONFIG_INI"
[ENTER]
yaml_file_path = $CONFIG_FILE
lang = en
EOL

# Create a launcher script
LAUNCHER_SCRIPT="/usr/local/bin/enter"
success "Creating a launcher script..."
cat <<EOL | sudo tee "$LAUNCHER_SCRIPT" > /dev/null
#!/bin/bash
$(pwd)/venv/bin/python -m src "\$@"
EOL

# Make the launcher script executable
sudo chmod +x "$LAUNCHER_SCRIPT" || error "Error: Failed to make the launcher script executable."

# Completion message
success "Installation completed successfully!"
echo -e "You can now use Enter as a command. Try the following:"
echo -e "1. List all aliases: ${GREEN}enter --list${NC}"
echo -e "2. Show alias details: ${GREEN}enter --info <alias_name>${NC}"
echo -e "3. Execute an alias: ${GREEN}enter <alias_name> [arguments]${NC}"
echo -e "Example: ${GREEN}enter hello name=John place=World${NC}"