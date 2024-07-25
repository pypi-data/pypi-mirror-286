Cisco Router NETCONF Script

This Python script retrieves configuration data from a Cisco router using NETCONF. It utilizes the ncclient library for NETCONF communication and optionally leverages Google's Generative AI service (currently Gemini) for XML request generation.

Features:

    Connects to Cisco IOS XE or IOS XR routers.
    Retrieves configuration data using NETCONF.
    Extracts leaf nodes from the configuration data.
    Allows user selection of specific attributes through:
        Line number from a generated file.
        Attribute name search.
    Creates the corresponding NETCONF XML request (optional, uses Google Generative AI).

Installation:

Bash

Plain Text

pip install -r requirements.txt

Usage:

    Configure Script:
        Update GOOGLE_API_KEY environment variable with your Google API key (optional for Generative AI).
        Edit main function to specify Cisco router version (IOS XE or IOS XR).
    Run Script:
        Execute python main.py
    Follow Prompts:
        Provide router details (IP, username, password).
        Select attributes for retrieval (optional, uses Google Generative AI).

Dependencies:

    ncclient
    xmltodict
    argparse
    langchain (optional, for Generative AI)
