from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.shortcuts import choice, prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator
from prompt_toolkit.filters import is_done
from typing import Tuple
from pathlib import Path
from enum import Enum
import re
import courses as Courses
import actions as Actions


def main():
    # Establish Global State
    global last_actions
    last_actions = []

    global STYLE
    STYLE = Style.from_dict(
        {
            "frame.border": "#b4befe",
            "selected-option": "bold",
        }
    )

    # Execute Program
    course = choose_course_from("/home/j/university/@current-semester")
    if course == "exit":
        return

    action = choose_action_from(MainActions)
    if action == "exit":
        return

    action.run_with(course)


class ActionEnum(Enum):
    """
    An Action is a tuple of (str, (X -> any)) where X is a Course
    The string is a display message describing the action
    The unary function is the action to execute

    All children of Action must be Enum such they follow a similar format as:
    class ChildOfAction(Action):
        ACTION_1 = ("Message", lambda x: x)
        ...
    """

    def display(self):
        """
        display returns the message describing what the action does.
        Return      - str
        """
        assert (
            type(self.value[0]) == str
        ), f"The Action, {self.name} is malformed, first argument of tuple is not string."
        return self.value[0]

    def run_with(self, course: Courses.Course):
        """
        run_with applys the action's function to a given course
        course      - Course
        returns     - any
        """
        assert callable(
            self.value[1]
        ), f"The Action, {self.name} is malformed, second argument of tuple is not callable."
        return self.value[1](course)


def choose_course_from(path):
    """
    choose_course finds all the courses in the given directory path
                  and prompts the user to select a course using a choice widget
                  returns the chosen Course or "exit"
    Returns      - Course or str
    Side Effects - Reads from Input
    """
    courses = sorted(
        Courses.find_all_courses(path),
        reverse=True,
    )

    return choice(
        message=HTML("<u>Select a class</u>:"),
        options=[
            (course, f"{course.designator} {course.code}: {course.course_title}")
            for course in courses
        ]
        + [("exit", "Exit")],
        style=STYLE,
        show_frame=True,
        bottom_toolbar=HTML(
            "Press <b>j/k</b> to move <b>up/down</b> | Press <b>Enter</b> to <b>Select</b>"
        ),
    )


def action_to_option(action: ActionEnum) -> Tuple[ActionEnum, str]:
    """
    action_to_option transforms a given action into a valid option
                     for prompt toolkit selection.
    action      - A valid Action
    returns     - (Action, str)
    """
    return (action, action.display())


def choose_action_from(actions) -> ActionEnum:
    """
    choose_action prompts the user to select a valid action to perform using a
                  choice widget
    actions     - Action Enum Class
    Returns     - Action
    Side Effects: Reads from Input
    """
    options = [action_to_option(action) for action in actions]
    last_actions.append(actions)
    return choice(
        message=HTML("<u>Choose an action</u>:"),
        options=options,
        style=STYLE,
        show_frame=True,
        bottom_toolbar=HTML(
            "Press <b>j/k</b> to move <b>up/down</b> | Press <b>Enter</b> to <b>Select</b>"
        ),
    )


def format_lecture_str(lecture: Courses.Lecture):
    return HTML(f"<b>{lecture.title:<56}</b> {lecture.creation_date}")


def lecture_to_option(lecture: Courses.Lecture):
    """
    lecture_to_option transforms a given lecture into a valid option
                      for prompt toolkit selection.
    Lecture     - A valid Lecture
    returns     - (Lecture, str)
    """
    return (lecture, format_lecture_str(lecture))


def choose_lecture_from(course: Courses.Course):
    """
    choose_lecture_from prompts the user to select a lecture using a
                        choice widget, returns selected lecture or
                        "exit"
    course      - Course
    returns     - One of Lecture or str
    Side Effects: Reads from Input
    """
    options = [lecture_to_option(lecture) for lecture in course.lectures]
    return choice(
        message=HTML("<u>Choose a lecture</u>:"),
        options=options + [("exit", "Exit")],
        style=STYLE,
        show_frame=True,
    )


"""
A string s is a valid Range if the following conditions are met:
Note: This definition of range is inclusive on both ends
   1) s is of the form "[num1]-[num2]"
   2) num1 <= num2
   3) num1 >= minimum
   4) num2 <= maximum
"""


def is_valid_range(s: str, minimum: int, maximum: int) -> bool:
    """
    is_valid_range returns True if the given string s is a valid range
    s       - str
    minimum - int
    maximum - int
    returns - bool
    """
    con1 = lambda s: re.search(r"\d+-\d+", s) is not None
    con2 = lambda s: int(s.split("-")[0]) <= int(s.split("-")[1])
    con3 = lambda s: int(s.split("-")[0]) >= minimum
    con4 = lambda s: int(s.split("-")[1]) <= maximum
    return con1(s) and con2(s) and con3(s) and con4(s)


def prompt_range(minimum: int, maximum: int) -> Tuple[int, int]:
    """
    prompt_range prompts for a valid range from user input between two
                 given values. Returns the lower and upper bounds of
                 the range as a tuple in the form (lower, upper)
    minimum     - int
    maximum     - int
    returns     - (int, int)
    """
    assert minimum <= maximum

    validator = Validator.from_callable(
        lambda s: is_valid_range(s, minimum, maximum),
        error_message="Not a valid range.",
        move_cursor_to_end=True,
    )
    text = prompt(
        HTML("<b>></b> "),
        validator=validator,
        style=STYLE,
        cursor=CursorShape.BLINKING_BLOCK,
        bottom_toolbar=HTML(
            f"Enter a range in the form: [num]-[num] between {minimum} and {maximum}"
        ),
    )
    values = text.split("-")
    lower = int(values[0])
    upper = int(values[1])
    return (lower, upper)


def prompt_lecture_range(course: Courses.Course):
    if len(course.lectures) == 0:
        print(f"No lecture notes found for {course.designator} {course.code}.")
        return
    for lecture in course.lectures:
        print_formatted_text(f"({lecture.lecture_num}) ", format_lecture_str(lecture))

    # Valid ranges are between 1 and len(course.lectures)
    Actions.lecture_open_range(course, *prompt_range(1, len(course.lectures)))


def lecture_view(course: Courses.Course):
    if len(course.lectures) == 0:
        print(f"No lecture notes found for {course.designator} {course.code}.")
    choice = choose_lecture_from(course)
    if choice == "exit":
        return
    Actions.edit_lecture(course, choice)


def go_back(course: Courses.Course):
    """
    go_back is a unary function that traverses to the previous set
            of actions by reading from the global state "last_actions"
    course      - Course, selected initially
    returns     - None

    Side Effects: Mutates last_actions by popping the last 2 entries off
    """
    last_actions.pop()  # Pop once to remove the page just visited
    # Pop again to get the previously visited set of actions
    return choose_action_from(last_actions.pop()).run_with(course)


# Global Constant Action
GO_BACK_ACTION = ("Go Back to Previous Page", go_back)


class LectureActions(ActionEnum):
    ALL = ("Compile All Lecture Notes", Actions.lecture_open_all)
    RANGE = ("Compile Notes from Range", prompt_lecture_range)
    VIEW = ("View and Edit Specific Note", lecture_view)
    BACK = GO_BACK_ACTION


class MainActions(ActionEnum):
    NEW = ("Create a New Note and Open in Neovim", Actions.create_new_note)
    OPEN = (
        "View Previous Lecture Notes",
        lambda course: choose_action_from(LectureActions).run_with(course),
    )
    EDIT = ("Edit Last Lecture's Notes", Actions.edit_last_lecture)
    EXPLORER = ("Open Course Directory", Actions.open_directory)
    WEB = ("Open Course Page", Actions.open_course_page)
    EXIT = ("Exit", lambda x: x)


if __name__ == "__main__":
    main()
