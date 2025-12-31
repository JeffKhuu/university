# Typst + Python + Bash Notetaking TUI

# Initial Setup
1. Install `yq` to parse yaml files in the terminal.
2. Clone the project repository
```bash
sudo snap install yq
```
2. Follow the steps below to link a semester directory
3. Move the courses script into a valid binaries directory. For example from the `scripts` directory,
```bash
mv courses ~/.local/bin/
```
4. Use the `courses` to run the TUI

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
