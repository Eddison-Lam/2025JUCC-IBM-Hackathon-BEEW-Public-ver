# 2025JUCC-IBM-Hackathon-BEEW-Public-ver
public version of my team in JUCC cross IBM hackathon (specific algorithm only visible in private version).
collaborators: bobbyleung1225, EthanNotEven, Fewsnowxd 

# International Exchange Program Matcher

## Overview
This project is a web-based application designed to match students with international exchange programs based on their qualifications and preferences. Built for the 2025 JUCC Hackathon, it features a modern Streamlit interface, data visualization with Plotly, and cross-platform setup scripts for Windows and Linux/macOS. The application processes student and program data to generate optimal matches, showcasing skills in Python, web development, and automation.

**Note**: This public repository contains the frontend and setup components. The full project, including AI-driven matching logic, is available in a private repository for authorized collaborators. Contact me for demo access.

## Features
- **User Interface**: Streamlit-based dashboard for uploading student/program data and viewing match results.
- **Data Visualization**: Interactive charts (e.g., pie charts) to display match distribution.
- **Cross-Platform Setup**: Automated scripts to check and install dependencies on Windows and Linux/macOS.
- **Modular Design**: Clean, maintainable code with a focus on user experience.

## Requirements
- **Python**: Version 3.11.9 or above
- **MySQL**: Version 8.0.42 (or compatible, e.g., 8.0.x for Linux/macOS)
- **Dependencies**: Listed in `requirements.txt`

### Auto Installation
- **Windows**: Run `check_install.bat` to verify/install Python and prompt for MySQL setup.
- **Linux/macOS**: Run `check_install.sh` to install Python and MySQL via package managers (apt/Homebrew).

## How to Run
1. Clone this repository: `git clone <public-repo-url>`
2. Install dependencies: Run `start_app.bat` (Windows) or `start_app.sh` (Linux/macOS). This installs libraries from `requirements.txt` and launches the Streamlit app.
3. Open the app in your browser (typically `http://localhost:8501`).
4. Upload sample CSV files (format described in the app) to test the interface.

## Output
- Displays a table of student-to-program matches and a pie chart of match rate.
- Export results as CSV or a summary report.

**Performance**: The UI is responsive, but full matching logic (in private repo) may take O(n²) time due to gale-shapley algorithm.

## Project Structure
- `ui.py`: Streamlit frontend for data input and result visualization.
- `start_app.bat`, `start_app.sh`: Scripts to install dependencies and run the app.
- `check_install.bat`, `check_install.sh`: Scripts to verify/install Python and MySQL.
- `uninstall_dependence.bat`: Utility to remove dependencies.
- `requirements.txt`: Python library dependencies.

## Notes
- This public version excludes proprietary AI matching algorithms and database logic.
- For a live demo or access to the full project, contact me to request a GitHub collaborator invite or Codespaces demo.
- Licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) to restrict reuse.

## Acknowledgments
Built as part of the 2025 JUCC Hackathon. Powered by Streamlit, Plotly, ibm_watsonx_ai and Python.
