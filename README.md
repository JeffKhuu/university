# Typst + Python + Bash Notetaking TUI
TUI written in prompt-toolkit python utilzing Typst for typsetting

# Initial Setup
1. Install `yq` to parse yaml files in the terminal.
2. Install `typst` for notetaking
2. Clone the project repository
3. Create a Python 
4. Move the courses script into a valid binaries directory.
5. Move the Typst package into a local packages directory.

```bash
sudo snap install typst
sudo snap install yq
git clone https://github.com/JeffKhuu/university.git
python3 -m venv venv
mv courses ~/.local/bin/
mv lecture-notes-core ~/.local/share/typst/packages/local/
```
2. Follow the steps under *Setup for New Semesters* below to link a semester directory
4. Use the `courses` command to run the TUI

# Setup for New Semesters
0. Ensure you're in the root project directory. (i.e the parent of the `scripts` directory)
1. Change the current-semester symlink to the directory of the new semester
```bash
./scripts/link-semester.sh /path/to/semester
```
2. Create directories corresponding to each course for the semester.
3. Create an `info.yaml` file in each course directory with the following format
```yaml
title: TITLE
designator: DESIGNATOR
code: CODE
url: URL
```
4. Activate the Python virtual environment and initiate each course
```bash
source ./scripts/venv/bin/activate
python3 ./scripts/init_all_courses.py
```
