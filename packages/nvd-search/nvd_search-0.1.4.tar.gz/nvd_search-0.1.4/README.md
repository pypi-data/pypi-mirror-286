# NVD SEARCH TOOL

## Overview

`nvd-search` is a Python tool designed to fetch and process data from the National Vulnerability Database (NVD) API v2. This tool is made using the best practices suggested by the NIST.

## Features

- Fetch data from the NVD API
- Maintain the database and keep it updated

## Installation

### Prerequisites
- Request an NVD API KEY , and then export it :
```bash
    export NVD_API_KEY=api_key
``` 
- Python 3.10 or higher.
- Poetry (for package management).
- MongoDB as database for this tool.

### Steps for using this tool with Poetry

1. **Clone the repository**:
    ```bash
    git clone https://github.com/khalilbouzoffara/nvd-search.git
    cd nvd-search
    ```

2. **Install dependencies**:
    ```bash
    poetry install
    ```

3. **Activate the virtual environment**:
    ```bash
    poetry shell
    ```
### Use this tool as a python package

You can use this tool also as a python package
    
    pip install nvd-search
    

## Usage

You can run this command to help you explore this tool:

```bash
nvd-search --help
```