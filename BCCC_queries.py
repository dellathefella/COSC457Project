from tkinter import *
from tkinter.ttk import *
import mysql.connector
import asyncio
from typing import *

# Database Credentials
db = mysql.connector.connect(
    host="epsilon1.duckdns.org",
    user="cosc457user",
    password="ERDSaresofun",
    database="cosc457"
)


# Create window object
app = Tk()

# Styles
style = Style()
style.configure("Error.TLabel", foreground="red", font=("bold", 12))
style.configure("TButton", font=("bold", 12), padding=10)

# Hold the results from our database queries
results: List[Tuple[str, ...]] = []


def query1(params: Dict[str, str]) -> str:
    return """
        SELECT
            title
        FROM
            Course_christian
        WHERE
            code IN (
                SELECT
                    course_code
                FROM
                    Program_Courses_christian
                WHERE
                    program_id = (
                        SELECT
                            id
                        FROM
                            Program_christian
                        WHERE
                            name = "{Program_name}"
                    )
            );
        """.format(**params)


def query2(params: Dict[str, str]) -> str:
    # Fall:     August 24th - December 14th
    # Winter:   January 4th - January 22nd
    # Spring:   January 25th - May 18th
    # Summer:   May 24th - August 3rd
    #
    # We're only looking for the semester, not the year, so the default
    # year will always be 2020 since it doesn't matter.
    #
    # Calculate dates based off of semester:
    date_start = ''
    date_end = ''
    if (params['Section_semester'].lower() == 'fall'):
        date_start = '2020-08-24'
        date_end = '2020-12-14'
    elif (params['Section_semester'].lower() == 'winter'):
        date_start = '2020-01-04'
        date_end = '2020-01-22'
    elif (params['Section_semester'].lower() == 'spring'):
        date_start = '2020-01-25'
        date_end = '2020-05-18'
    elif (params['Section_semester'].lower() == 'summer'):
        date_start = '2020-05-24'
        date_end = '2020-08-03'
    else:  # default to all courses
        date_start = '2020-01-01'
        date_end = '2020-12-31'
        print("[!] Invalid semester entered! Defaulting to all courses...")

    return """
        SELECT
            code,
            title
        FROM
            Course_christian
        WHERE
            dep_num = (
                SELECT
                    dep_num
                FROM
                    Department_christian
                WHERE
                    name = "{Department_name}"
            )
            AND code IN (
                SELECT
                    course_code
                FROM
                    Section_christian
                WHERE
                    DAYOFYEAR(date_start) >= DAYOFYEAR("{Section_date_start}")
                    AND DAYOFYEAR(date_end) <= DAYOFYEAR("{Section_date_end}")
            );
        """.format(Department_name=params["Department_name"], Section_date_start=date_start, Section_date_end=date_end)


def query3(params: Dict[str, str]) -> str:
    return """
        SELECT
            fname,
            lname
        FROM
            Id_christian
        WHERE
            id IN (
                SELECT
                    id_card
                FROM
                    Staff_christian
                WHERE
                    id IN (
                        SELECT
                            instructor_id
                        FROM
                            Section_christian
                        WHERE
                            course_code IN (
                                SELECT
                                    course_code
                                FROM
                                    Program_Courses_christian
                                WHERE
                                    program_id = (
                                        SELECT
                                            id
                                        FROM
                                            Program_christian
                                        WHERE
                                            name = "{Program_name}"
                                    )
                            )
                    )
            );
        """.format(**params)


def query4(params: Dict[str, str]) -> str:
    return """
        SELECT
            fname,
            lname
        FROM
            Id_christian
        WHERE
            id IN (
                SELECT
                    id_card
                FROM
                    Staff_christian
                WHERE
                    id IN (
                        SELECT
                            advisor_id
                        FROM
                            Department_christian
                    )
                    OR id IN (
                        SELECT
                            advisor_id
                        FROM
                            Student_christian
                    )
            );
        """


def query5(params: Dict[str, str]) -> str:
    print("Query 5!")


def query6(params: Dict[str, str]) -> str:
    print("Query 6!")


def query7(params: Dict[str, str]) -> str:
    print("Query 7!")


def query8(params: Dict[str, str]) -> str:
    print("Query 8!")


def query9(params: Dict[str, str]) -> str:
    print("Query 9!")


def query10(params: Dict[str, str]) -> str:
    print("Query 10!")


# List of all possible queries
# Description, Parameters needed, Query function
#
# If the attribute you need is, for example,'Program -> name', use the naming convention 'Program_name'
query_dict = {
    1:  ("List the names of the courses offered by a specific program.", ["Program_name"], query1),
    2:  ("List what courses are offered in a specific department during a specific semester.", ["Section_semester", "Department_name"], query2),
    3:  ("List the first and last names of staff that teach a course in a specific program.", ["Program_name"], query3),
    4:  ("List the first and last names of staff that are also an advisor.", [], query4),
    5:  ("List the first and last names of students who have a specific staff member as an advisor.", [], query5),
    6:  ("Retrieve how many students withdrew/dropped a specific course during a specific semester.", [], query6),
    7:  ("Generate a list of professsors who have taught at Baltimore City Community College for >= five years as of a specific semester.", [], query7),
    8:  ("List all of the first and last names of students enrolled in a specific program who are female.", [], query8),
    9:  ("Find the name of the student who has a specific ID no.", [], query9),
    10: ("List the grade records of all of the courses during a specific semester for a particular student.", [], query10)
}


class Dialog:
    def __init__(self, main, params_needed: List[str]):
        popup = self.popup = Toplevel(main)
        popup.title("Enter parameters")

        params_box = self.params_box = Frame(popup, padding=[10, 10])
        params_box.pack()

        self.entries = {}
        for num, param_name in enumerate(params_needed):
            # Replace the underscores with spaces for nicer display
            param_name_split = param_name.split("_")
            Label(params_box, anchor=W, text=" ".join(
                param_name_split) + ":").grid(row=num, column=0)
            e = Entry(params_box)
            e.grid(row=num, column=1)
            self.entries[param_name] = e

        button_frame = self.button_frame = Frame(popup, padding=[0, 10])
        button_frame.pack()
        Button(button_frame, text="Submit",
               command=self.pull_data_from_entries).pack()

        self.params = {}
        self.error = None

    def pull_data_from_entries(self) -> None:
        for entry_name in self.entries:
            if not self.entries[entry_name].get():
                # Don't show error if it's already showing
                if not self.error:
                    # Show error
                    self.error = Label(
                        self.popup, text="Please provide all parameters", style="Error.TLabel")
                    self.error.pack()
                return
            else:
                self.params[entry_name] = self.entries[entry_name].get()
        self.popup.destroy()


class App:
    def __init__(self, app):
        main = self.main = app

        # Define left and right halves
        left_frame = self.left_frame = Frame(main, padding=[20, 0])
        right_frame = self.right_frame = Frame(main, padding=[20, 0])
        left_frame.grid(row=0, column=0)
        right_frame.grid(row=0, column=1)

        title_frame = self.title_frame = Frame(left_frame, padding=[0, 10])
        title_frame.pack()
        Label(title_frame, text="Select your query below:",
              font=("bold", 12), padding=[0, 10]).pack()
        self.query_error = Label(
            self.title_frame, text="Please select a query", style="Error.TLabel")

        # Frame for list of available queries
        query_list_frame = self.query_list_frame = LabelFrame(
            left_frame, text="Query list")
        query_list_frame.pack()

        query_num = self.query_num = IntVar(0)
        for i in range(1, len(query_dict)+1):
            Radiobutton(query_list_frame,
                        text=query_dict[i][0], variable=query_num, value=i).pack(anchor=W)

        execute_button_frame = self.execute_button_frame = Frame(
            left_frame, padding=[0, 10])
        execute_button_frame.pack()
        execute_button = self.execute_button = Button(
            execute_button_frame, text="Execute query", command=lambda: self.run_query(query_num.get()))
        execute_button.pack()

        # Right frame results list
        Label(
            right_frame, text="This is a test label that is a lot longer than the other text!").pack()
        Label(right_frame, text="This is where the results should show up, ideally with a scrollbar for long lists.").pack()

    # Currently only Queries 1, 2, 3 work, which is checked for here for debugging purposes.
    # Any other Queries just print "Query X!"
    def run_query(self, query_num):
        if (query_num < 1):
            # Show error if not already visible
            if not self.query_error.winfo_viewable():
                # Show error
                self.query_error.pack()
        else:
            self.execute_button["state"] = "disabled"
            # Hide error if visible
            if self.query_error.winfo_viewable():
                self.query_error.pack_forget()
            # if (query_num <= 3):
            cursor = db.cursor()
            params: Dict[str, str] = []
            params_needed: List[str] = query_dict[query_num][1]
            if (params_needed):
                dialog = Dialog(self.main, params_needed)
                self.main.wait_window(dialog.popup)
                params = dialog.params
                del dialog  # we don't need it any more, created per-query
                # If we close the window early (press X on window), don't run the query
                if (len(params) != len(params_needed)):
                    self.execute_button["state"] = "normal"
                    return
            print("[=] params = " + str(params))
            cursor.execute(query_dict[query_num][2](params))
            results.clear()
            for result in cursor:
                results.append(result)

            print("[+] " + str(results) + "\n")
            # else:
            #    query_dict[query_num][1]()
            self.execute_button["state"] = "normal"


# Currently results are just printed to console
if __name__ == "__main__":
    # Configure window settings
    app.title("BCCC Database Interactions")

    # Connect to our database
    db.connect

    # Create the main window class
    main_window = App(app)

    # Start the program
    app.mainloop()
