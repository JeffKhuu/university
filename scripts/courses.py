from datetime import date
import yaml
import os
import typst
import json

"""
A valid CourseDirectory has:
- an info.yaml file
"""


class Course:
    """
    A Course has the following attributes:
    path            - str
    course_title    - str
    url             - str
    designator      - str
    code            - str
    lectures        - list of Lecture
    """

    def __init__(self, path) -> None:
        """
        path - A path to a valid CourseDirectory
        """
        info = yaml.safe_load(open(f"{path}/info.yaml"))
        # info is a dictionary with the following keys: title, url, designator, code

        self.path = os.path.abspath(path)
        self.course_title = info["title"]
        self.url = info["url"]
        self.designator = info["designator"]
        self.code = info["code"]
        self.lectures = sorted(find_all_lectures(self.path))

    def __gt__(self, c2):
        if self.designator == c2.designator:
            return int(self.code) > int(c2.code)
        return self.designator > c2.designator

    def __repr__(self) -> str:
        return f"<{self.designator} {self.code}>"


class Lecture:
    """
    A Lecture has the following attributes:
    title           - str
    lecture_num     - int
    creation_date   - datetime.date
    """

    def __init__(self, title: str, lecture_num: int, creation_date: date) -> None:
        self.title = title
        self.lecture_num = lecture_num
        self.creation_date = creation_date

    def __gt__(self, l2):
        return self.lecture_num > l2.lecture_num

    def __repr__(self) -> str:
        return f"<{self.lecture_num} {self.title}>"


def find_all_lectures(path):
    """
    find_all_lectures finds all valid lecture files in a given file path
                      a valid lecture file is of the form "lec_#.typ"
                      where # is an integer
    path    - A valid path
    returns - List of Lecture
    """
    lecture_file_names = [
        file.name for file in os.scandir(path) if is_lecture_note(file)
    ]
    lectures: list[Lecture] = []
    for file_name in lecture_file_names:
        try:
            lecture_title = json.loads(
                typst.query(f"{path}/{file_name}", "<title>", field="value", one=True)
            )
            lecture_num = int(file_name[4])
            creation_date_str = json.loads(
                typst.query(
                    f"{path}/{file_name}", "<creation_date>", field="value", one=True
                )
            )
            creation_date = date.fromisoformat(creation_date_str)
            lecture = Lecture(lecture_title, lecture_num, creation_date)
            lectures.append(lecture)
        except:
            print(f"An error occured when processing {file_name} in {path.split("/")[-1]}. Possible malformed lecture template.")

    return lectures


is_lecture_note = (
    lambda f: f.is_file() and f.name.startswith("lec") and f.name.endswith(".typ")
)


def find_all_courses(path):
    """
    find_all_courses finds all valid course directories in a given file path
    path    - A valid path
    returns - List of Course
    """
    subdir_paths = [f.path for f in os.scandir(path) if f.is_dir]
    courses: list[Course] = []
    for path in subdir_paths:
        try:
            course = Course(path)
            courses.append(course)
        except:
            print(f"Skipping ./{path.split("/")[-1]}, no info.yaml found.")
    return courses
