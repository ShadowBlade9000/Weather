PROJECT STRUCTURE

weather.py : Main Python weather application.

README.txt : Setup and installation instructions.

INSTALLATION BY OPERATING SYSTEM

--- ARCH LINUX / MANJARO ---

Open your terminal and install the required dependencies:

sudo pacman -S tk python-requests python-pillow

Run the application:

python weather.py

--- UBUNTU / DEBIAN / LINUX MINT ---

Open your terminal and install dependencies:

sudo apt update
sudo apt install python3-tk python3-requests python3-pil

Run the application:

python3 weather.py

--- FEDORA / RHEL / CENTOS ---

Open your terminal and install dependencies:

sudo dnf install python3-tkinter python3-requests python3-pillow

Run the application:

python3 weather.py

--- WINDOWS ---

Download and install Python from https://www.python.org/downloads/
(Ensure "Add Python to PATH" is checked during setup).

Open Command Prompt or PowerShell and install required packages:

pip install requests pillow

Run the application:

python weather.py

--- MACOS ---

Open Terminal.

Install dependencies:

pip3 install requests pillow

(Note: Tkinter comes bundled with official Python installers from python.org.
If using Homebrew Python, run: brew install python-tk)

Run the application:

python3 weather.py