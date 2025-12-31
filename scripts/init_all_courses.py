import courses as Courses
import os
from pathlib import Path


def main():
    courses = Courses.find_all_courses(
        str(Path.home()) + "/university/@current-semester"
    )
    for course in courses:
        os.makedirs(course.path + "/Figures", exist_ok=True)
        try:
            with open(course.path + "/utils.typ", "x") as f:
                f.write(
                    '#import "@local/lecture-notes-core:1.0.0": *'
                )  # Add required notetaking dependency
        except FileExistsError:
            print(f"{course.designator} {course.code} already has a utils.typ file.")


if __name__ == "__main__":
    main()
