from courses import Course, Lecture
import subprocess
import datetime


def create_new_note(course: Course):
    lec_num = get_last_lecture(course)
    next_lec = lec_num + 1
    # Create the .typ file
    try:
        with open(course.path + f"/lec_{next_lec}.typ", "x") as f:
            # Add notetaking snippets
            f.write('#import "utils.typ": *\n')
            # Instantiate document template, passing in lecture num, title, info.yaml and the document
            f.write(
                f'#show: doc => template(\n\t{next_lec}, \
                \n\t"TITLE", \
                \n\t"{course.designator} {course.code}", \
                \n\t{get_current_date()}, \
                \n\tdoc\n)'
            )
    except IOError:
        print("Something went wrong creating the note. Please try again.")

    # Open neovim
    subprocess.run(["nvim", f"{course.path}/lec_{next_lec}.typ"])


def open_course_page(course: Course):
    subprocess.run(["explorer.exe", course.url])


def open_directory(course: Course):
    path = get_wsl_path(course.path)
    subprocess.run(["explorer.exe", path])

def lecture_open_range(course: Course, lower: int, upper: int):
    """
    lecture_open_range compiles a 'preview.pdf' in the root folder including
                       lectures numbered from lower to upper inclusively
    course      - Course
    lower       - int
    upper       - int
    returns     - None
    """
    if lower == 0 or upper == 0:
        print(f"No lecture notes found for {course.designator} {course.code}.")
        return
    # Use the path to the courses to find the find to the root folder (with preview.typ)
    preview_path = "/".join(course.path.split("/")[:4])

    # Typst Compile uses a relative path from the directory of the preview typst file
    # Splice for the last two relevant parts of the path (i.e. [semester]/[class])
    path = "/".join(course.path.split("/")[-2:])
    subprocess.run(
        [
            "typst",
            "compile",
            f"{preview_path}/preview.typ",
            "--input",
            f"min={lower}",
            "--input",
            f"max={upper}",
            "--input",
            f"path=/{path}/",
        ]
    )  # Compile the document

    # Open the document
    subprocess.run(["explorer.exe", get_wsl_path(preview_path + "/preview.pdf")])


def lecture_open_all(course: Course):
    """
    open_last_lecture compiles a 'preview.pdf' of all created lecture note
    course      - Course
    returns     - None
    """
    lec_num = get_last_lecture(course)
    return lecture_open_range(course, 1, lec_num)



def edit_last_lecture(course: Course):
    lec_num = get_last_lecture(course)
    # Open neovim
    subprocess.run(["nvim", f"{course.path}/lec_{lec_num}.typ"])

def edit_lecture(course: Course, lecture: Lecture):
    subprocess.run(["nvim", f"{course.path}/lec_{lecture.lecture_num}.typ"])


def get_wsl_path(path):
    """
    get_wsl_path returns the windows path from a given WSL unix path
    path        - Unix path
    returns     - Windows path
    """
    process = subprocess.run(["wslpath", "-w", path], capture_output=True)
    if process.returncode != 0:
        raise Exception("Something went wrong processing the path.")
    return process.stdout


def get_current_date():
    """
    get_current_date reads and returns a string for the constructor of a Typst
                     datetime object for the current date
    Examples:
        # If the date is September 1st 2025
        get_current_date() -> "datetime(year: 2025, month: 9, day: 1)"
    """
    date = datetime.date.today()
    return f"datetime(year: {date.year}, month: {date.month}, day: {date.day})"


def get_last_lecture(course: Course):
    """
    get_last_lecture returns an integer representing the last created lecture note
                     starting from 1, returns 0 if no lecture notes are found
    course      - Course
    returns     - int
    """
    if course.lectures:  # checks if lecture_files is empty
        return course.lectures[-1].lecture_num
    return 0
