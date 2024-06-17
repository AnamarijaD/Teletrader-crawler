# Web-crawler

This Python service downloads PDF fund documents from a specific website once a day and saves them to a file. Additionally, the metadata of the downloaded files is saved in a CSV file.

## Features

- Automatically downloads PDF fund documents from a specified website daily.
- Saves the downloaded PDFs to a specified directory.
- Extracts and saves metadata of the downloaded files (e.g., filename, download timestamp, file size) to a CSV file.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `schedule`
- `pandas`

## Installation

1. Clone the repository:

   ```sh
   git clone [repository_url]
   cd [repository_directory]
   
2. Create and activate a virtual environment:

   ```sh
   python -m venv env
   .\env\Scripts\activate  # On Windows
   source env/bin/activate  # On macOS/Linux

4. Install the required packages:

   ```sh
   pip install -r requirements.txt

