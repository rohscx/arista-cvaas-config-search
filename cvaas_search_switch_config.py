"""
# Network Configuration Viewer
This application leverages the AristaCVAAS SDK to interact with network devices managed by Arista's CloudVision Portal (CVP). It reads and analyzes configurations from CVAAS-connected switches, matches specified text patterns within those configurations, and displays the results in a tabular format using Streamlit. The app also allows users to input custom text patterns for matching.
"""

import streamlit as st
import pandas as pd
import sys
import hmac
import streamlit as st
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from pyrad.packet import AccessRequest, AccessAccept

def check_password():
    """Returns `True` if the user had a correct password using RADIUS server."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Sends a RADIUS request to check if the username and password are correct."""
        client = Client(server="127.0.0.1", secret=b"testing123", dict=Dictionary("./radius.dict"))
        client.AuthPort = 1812  # Default port, adjust if your server uses a different one

        req = client.CreateAuthPacket(code=AccessRequest, User_Name=st.session_state["username"])
        req["User-Password"] = req.PwCrypt(st.session_state["password"])

        try:
            reply = client.SendPacket(req)
            if reply.code == AccessAccept:
                st.session_state["password_correct"] = True
            else:
                st.session_state["password_correct"] = False
        except Exception as e:
            st.error("Failed to authenticate with RADIUS server: " + str(e))
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 User not known or password incorrect")
    return False

if not check_password():
    st.stop()

# Main Streamlit app starts here
# Adding the SDK directory to the Python path for import
sys.path.insert(1, './arista-cvaas-sdk/')
from arista_cvaas_sdk import AristaCVAAS  # Import the SDK

# Streamlit function to display app title
st.write("Search CVAAS Switch configuration")

# Reading authentication token from a local file and stripping any extraneous whitespace
with open('./auth_token', 'r') as file:
    auth_token = file.read().strip()

# Configuration of API access details:
server_url = "https://www.arista.io"
api = AristaCVAAS(server_url, auth_token)  # Creating an instance of the AristaCVAAS class with the server URL and auth token

# Retrieve and display general information about the CVP environment
api.get_cvp_info()

# Cache the function to optimize data retrieval and reduce API calls during repeated access
@st.cache_data(show_spinner="Loading device Configs, please wait...")
def get_device_configs():
    # Collect configurations for each device in inventory; return as a list of tuples
    return [
        (x["hostname"], x["systemMacAddress"], api.get_inventory_device_config(x["systemMacAddress"])['output'])
        for x in api.get_inventory_devices()
    ]
# Text area for user input to specify a pattern to search within switch configurations
place_holder_text = r"""Example finds this route-map and matches any prepend:
  route-map BGP_ADV_ASE_QUAD permit 10
   description Quaternary advertised route-map
   set as-path prepend [ \d]+$"""
txt = st.text_area(
    "Text to match",
    placeholder=place_holder_text,
)

# Display the count of characters input by the user
st.write(f'You wrote {len(txt)} characters.')

# If user input is present, use it as the pattern; otherwise, use the default pattern
if txt:
    patterns = [txt.strip()]
else:
    patterns = [
        r"""route-map BGP_ADV_ASE_QUAD permit 10[ \t\n]+description Quaternary advertised route-map[ \t\n]+set as-path prepend [ \d]+""",
    ]

# Retrieve device configurations
data = get_device_configs()
results = []
# Process each device configuration to find matches to the specified patterns
for index, device in enumerate(sorted(data)):
    response = api.search_config_patterns(device[2], patterns, print_matches=False)
    for x in response:
        # Append each found match along with device details to the results list
        results.append({"Name": device[0], "Match": response[x]["matched"], "Config": response[x]['text']})

# Convert results to a DataFrame for better visualization
df1 = pd.DataFrame(results)

# Display the DataFrame using Streamlit, setting custom dimensions for better readability
st.dataframe(df1, width=900, height=900)
