# Not required but a virtual environment is recommended. The python file should be located in its own directory. From that directory create the virtual environment.
python3 -m venv ./venv
# Active the virtual environment
source venv/bin/activate
# if successful shell input should update 

## from

`➜  python_webapp`

## to

`(venv) ➜  python_webapp`

# To deactivate close the terminal window or issue this command
deactivate
# Install the required packages with the following command, you may need to use pip3 if you have not aliased it to pip.
pip install -r requirements.txt
# Populate the auth_token file with your CVAAS service account auth token. "https://www.arista.com/en/cg-cv/cv-service-accounts"

## It looks something like this:

`...I6IkpXVCJ9.eyJkaWQiOjcwODkzNDMxODEzNjM2NDI5MDcsImRzbiI6IkVyb3UiLCJkc3QiOiJhY2NvdW5...`

# Creating local user accounts
## Open this file and add users to the list. 
`.streamlit/secrets.toml`

## The key is the Username and the value is the Password
`alice_foo = "streamlit123"
 bob_bar = "mycrazypw"`

# SSL Certificate Generation Instructions

This README provides instructions on how to generate a `certchain.pem` and `private.key` for your application, tailored for macOS, Linux, and Windows.

## Common Requirements

Before proceeding, ensure you have OpenSSL installed on your system. If OpenSSL is not installed, please follow the installation instructions for your respective operating system.

### OpenSSL Installation

- **macOS**: OpenSSL is usually pre-installed; you can update or reinstall it via Homebrew if necessary:
  ```brew install openssl```
  
- **Linux**: Install OpenSSL using your distribution's package manager, for example, on Ubuntu/Debian:
 ```sudo apt update```
 ```sudo apt install openssl```
- **Windows:**: Download and install OpenSSL from OpenSSL official website

# Follow the instructions for your operating system.

# macOS and Linux
# Generate a Private Key
`openssl genrsa -out private.key 2048`
# Create a Certificate Signing Request (CSR)
`openssl req -new -key private.key -out certificate.csr`
# Generate a Self-Signed Certificate
`openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out certificate.pem`
`cp certificate.pem certchain.pem`

# Windows
# Generate a Private Key
`Open Command Prompt as Administrator and navigate to your OpenSSL installation directory, typically C:\Program Files\OpenSSL-Win64\bin\.`
# Generate a Private Key
`openssl genrsa -out private.key 2048`
# Create a Certificate Signing Request (CSR)
`openssl req -new -key private.key -out certificate.csr`
# Generate a Self-Signed Certificate
`openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out certificate.pem`
# Create the Certificate Chain File
`copy certificate.pem certchain.pem`

## Start streamlit by executing the python file
streamlit run cvaas_search_switch_config.py
