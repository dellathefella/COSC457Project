from tkinter import *
from tkinter.ttk import *
from typing import *
from sys import exit

import mysql.connector

# Database Credentials
db = mysql.connector.connect(
    host="epsilon1.duckdns.org",
    user="cosc457user",
    password="ERDSaresofun",
    database="cosc457",
)
cursor = db.cursor()


# Create window object
app = Tk()

# Styles
style = Style()
style.configure("Error.TLabel", foreground="red", font=("bold", 12))
style.configure("TButton", font=("bold", 12), padding=10)
# style.configure("TText", padding=10, font=("Consolas", 10))
style.configure("Treeview.Heading", foreground="red", font=("bold", 12))

style.configure("Test.TFrame", background="silver")


def semester_to_dates(semester: str, year: str) -> Tuple[str, str]:
    # Fall:     August 24th - December 14th
    # Winter:   January 4th - January 22nd
    # Spring:   January 25th - May 18th
    # Summer:   May 24th - August 3rd
    #
    # A "specific semester" contains a month-day range and a year.

    date_start, date_end = "", ""
    if semester.lower() == "fall":
        date_start = "{}-08-24".format(year)
        date_end = "{}-12-14".format(year)
    elif semester.lower() == "winter":
        date_start = "{}-01-04".format(year)
        date_end = "{}-01-22".format(year)
    elif semester.lower() == "spring":
        date_start = "{}-01-25".format(year)
        date_end = "{}-05-18".format(year)
    elif semester.lower() == "summer":
        date_start = "{}-05-24".format(year)
        date_end = "{}-08-03".format(year)
    else:  # default to entire year
        # We can do this because we have no semesters that wrap into other years
        date_start = "{}-01-01".format(year)
        date_end = "{}-12-31".format(year)
        print("[!] Invalid semester entered! Defaulting to entire year...")
    return (date_start, date_end)


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
        """.format(
        **params
    )


def query2(params: Dict[str, str]) -> str:
    # Calculate dates based off of semester:
    date_start, date_end = semester_to_dates(
        params["Section_semester"], params["Section_year"]
    )

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
                    date_start >= "{Section_date_start}"
                    AND date_end <= "{Section_date_end}"
            );
        """.format(
        Department_name=params["Department_name"],
        Section_date_start=date_start,
        Section_date_end=date_end,
    )


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
        """.format(
        **params
    )


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
                    Student_christian
                WHERE
                    advisor_id = (
                        SELECT
                            id
                        FROM
                            Staff_christian
                        WHERE
                            id_card = (
                                SELECT
                                    id
                                FROM
                                    Id_christian
                                WHERE
                                    fname = "{Advisor_fname}"
                                    AND lname = "{Advisor_lname}"
                            )
                    )
            );
        """.format(
        **params
    )


def query6(params: Dict[str, str]) -> str:
    # Calculate dates based off of semester:
    date_start, date_end = semester_to_dates(
        params["Section_semester"], params["Section_year"]
    )

    return """
        SELECT
            COUNT(student_id) AS num_students
        FROM
            Student_Sections_christian
        WHERE
            STATUS = "{Student_Sections_status}"
            AND section_id IN (
                SELECT
                    id
                FROM
                    Section_christian
                WHERE
                    course_code = "{Course_code}"
                    AND date_start >= "{Section_date_start}"
                    AND date_end <= "{Section_date_end}"
            );
        """.format(
        Student_Sections_status=params["Student_Sections_status"],
        Course_code=params["Course_code"],
        Section_date_start=date_start,
        Section_date_end=date_end,
    )


def query7(params: Dict[str, str]) -> str:
    date_start, date_end = semester_to_dates(
        params["Section_semester"], params["Section_year"]
    )
    # 1826 days = 365 days * 5 years + 1 leap day (at least one, could be two)
    return """
        SELECT
            fname,
            mname,
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
                    )
                    AND DATEDIFF("{semester_date_start}", date_hired) >= 1826
            );
        """.format(
        semester_date_start=date_start
    )


def query8(params: Dict[str, str]) -> str:
    return """
        SELECT
            fname,
            lname
        FROM
            Id_christian
        WHERE
            sex = "F"
            AND id IN (
                SELECT
                    id_card
                FROM
                    Student_christian
                WHERE
                    id IN (
                        SELECT
                            student_id
                        FROM
                            Program_Enrollment_christian
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
            );
        """.format(
        **params
    )


def query9(params: Dict[str, str]) -> str:
    return """
        SELECT
            fname,
            mname,
            lname
        FROM
            Id_christian
        WHERE
            id = (
                SELECT
                    id_card
                FROM
                    Student_christian
                WHERE
                    id = {Student_id}
            );
        """.format(
        **params
    )


def query10(params: Dict[str, str]) -> str:
    date_start, date_end = semester_to_dates(
        params["Section_semester"], params["Section_year"]
    )
    return """
        SELECT
            grade
        FROM
            Student_Sections_christian
        WHERE
            student_id = {Student_id}
            AND section_id IN (
                SELECT
                    id
                FROM
                    Section_christian
                WHERE
                    date_start >= "{Section_date_start}"
                    AND date_end <= "{Section_date_end}"
            );
        """.format(
        Student_id=params["Student_id"],
        Section_date_start=date_start,
        Section_date_end=date_end,
    )


# List of all possible queries
#
# num: (
#       "Displayed text",
#        ["List", "Of", "Parameters"],
#        function_name
# )
#
# If the attribute you need is, for example,'Program -> name', use the naming convention 'Program_name'
query_dict = {
    1: (
        "List the names of the courses offered by a specific program.",
        ["Program_name"],
        query1,
    ),
    2: (
        "List what courses are offered in a specific department during a specific semester.",
        ["Department_name", "Section_semester", "Section_year"],
        query2,
    ),
    3: (
        "List the first and last names of staff that teach a course in a specific program.",
        ["Program_name"],
        query3,
    ),
    4: ("List the first and last names of staff that are also an advisor.", [], query4),
    5: (
        "List the first and last names of students who have a specific staff member as an advisor.",
        ["Advisor_fname", "Advisor_lname"],
        query5,
    ),
    6: (
        "Retrieve how many students withdrew/dropped a specific course during a specific semester.",
        ["Student_Sections_status", "Course_code", "Section_semester", "Section_year"],
        query6,
    ),
    7: (
        "Generate a list of professsors who have taught at Baltimore City Community College for >= five years as of a specific semester.",
        ["Section_semester", "Section_year"],
        query7,
    ),
    8: (
        "List all of the first and last names of students enrolled in a specific program who are female.",
        ["Program_name"],
        query8,
    ),
    9: (
        "Find the name of the student who has a specific ID no.",
        ["Student_id"],
        query9,
    ),
    10: (
        "List the grade records of all of the courses during a specific semester for a particular student.",
        ["Student_id", "Section_semester", "Section_year"],
        query10,
    ),
}


class ParamsDialog:
    def __init__(self, main, params_needed: List[str]):
        popup = self.popup = Toplevel(main)
        popup.title("Enter parameters")

        self.title_frame = Frame(popup, padding=[0, 10])
        self.title_frame.pack()

        params_box = Frame(popup, padding=[10, 10])
        params_box.pack()

        self.entries = {}
        for num, param_name in enumerate(params_needed):
            # Replace the underscores with spaces for nicer display
            param_name_split = param_name.split("_")
            Label(params_box, text=" ".join(param_name_split) + ":").grid(
                row=num, column=0, sticky=E
            )
            e = Entry(params_box)
            e.grid(row=num, column=1, padx=10, pady=5)
            self.entries[param_name] = e

        button_frame = self.button_frame = Frame(popup, padding=[0, 10])
        button_frame.pack()
        Button(button_frame, text="Submit", command=self.pull_data_from_entries).pack()

        self.params = {}
        self.error = None

    def pull_data_from_entries(self) -> None:
        for entry_name in self.entries:
            if not self.entries[entry_name].get():
                # Don't show error if it's already showing
                if not self.error:
                    # Show error
                    self.error = Label(
                        self.title_frame,
                        text="Please provide all parameters",
                        style="Error.TLabel",
                    )
                    self.error.pack()
                return
            else:
                self.params[entry_name] = self.entries[entry_name].get()
        self.popup.destroy()


class QueryDialog:
    def __init__(self, main):
        popup = self.popup = Toplevel(main)
        popup.title("Custom query")

        self.title_frame = Frame(popup, padding=[0, 10])
        self.title_frame.pack()

        Label(
            self.title_frame,
            text="Type your query below. Be careful!",
            font=("bold", 12),
            padding=10,
        ).pack()

        self.query = StringVar()

        # For some reason Text() is returning a 'str' object and not the widget...?
        # query_box = Text(self.popup)

        entry_frame = Frame(popup, padding=10, style="Test.TFrame")
        entry_frame.pack(fill="both")
        Entry(entry_frame, textvariable=self.query).pack(fill="both")

        button_frame = self.button_frame = Frame(popup, padding=10)
        button_frame.pack()
        Button(button_frame, text="Submit", command=self.return_query).pack()

        self.error = None

    def return_query(self) -> str:
        if not self.query.get():
            if not self.error:
                self.error = Label(
                    self.title_frame,
                    text="Please enter your query",
                    style="Error.TLabel",
                )
                self.error.pack()
            return
        else:
            self.popup.destroy()


class App:
    def __init__(self, app):
        main = self.main = app

        # Define left and right halves
        left_frame = Frame(main, padding=[20, 0])
        left_frame.pack(side="left")

        right_frame = Frame(
            main, padding=20, width=600, height=360, style="Test.TFrame"
        )
        right_frame.pack_propagate(0)  # force dimensions
        right_frame.pack(side="right", fill="both")

        title_frame = Frame(left_frame, padding=[0, 10])
        title_frame.pack()
        Label(
            title_frame,
            text="Select your query below:",
            font=("bold", 12),
            padding=[0, 10],
        ).pack()
        # Error label
        self.error_label = Label(title_frame, text="", style="Error.TLabel")

        self.error_selection = "Please select a query"
        self.error_custom_syntax = "Query syntax incorrect"

        # Frame for list of available queries
        query_list_frame = LabelFrame(left_frame, text="Query list")
        query_list_frame.pack()

        query_num = IntVar(0)
        for i in range(1, len(query_dict) + 1):
            Radiobutton(
                query_list_frame, text=query_dict[i][0], variable=query_num, value=i
            ).pack(anchor=W)

        button_frame = Frame(left_frame, padding=10)
        button_frame.pack()
        button_spacer1 = Frame(button_frame, padding=10)
        button_spacer1.grid(row=0, column=0)
        button_spacer2 = Frame(button_frame, padding=10)
        button_spacer2.grid(row=0, column=1)
        execute_selected_button = self.execute_selected_button = Button(
            button_spacer1,
            text="Execute SELECTED query",
            command=lambda: self.run_selected_query(query_num.get()),
        )
        execute_selected_button.pack()
        execute_custom_button = self.execute_custom_button = Button(
            button_spacer2, text="Execute CUSTOM query", command=self.run_custom_query
        )
        execute_custom_button.pack()

        # Right frame results list
        results_table = self.results_table = Treeview(right_frame)

        # phantom column used for expanding labels
        results_table.column("#0", width=50, stretch=False)
        results_table.heading("#0", text="#", anchor=CENTER)

        # Results table scrollbars
        results_xscroll = Scrollbar(
            right_frame, orient="horizontal", command=results_table.xview
        )
        results_xscroll.pack(side="bottom", fill="x")
        results_vscroll = Scrollbar(
            right_frame, orient="vertical", command=results_table.yview
        )
        results_vscroll.pack(side="right", fill="y")
        results_table.configure(xscrollcommand=results_xscroll.set)
        results_table.configure(yscrollcommand=results_vscroll.set)

        results_table.pack(fill="both", expand=True)

    def run_selected_query(self, query_num):
        if query_num < 1:
            # Show error if not already visible
            self.error_label["text"] = self.error_selection
            if not self.error_label.winfo_viewable():
                # Show error
                self.error_label.pack()
        else:
            self.disable_buttons()
            # Hide error if visible
            if self.error_label.winfo_viewable():
                self.error_label.pack_forget()
            params: Dict[str, str] = []
            params_needed: List[str] = query_dict[query_num][1]
            if params_needed:
                dialog = ParamsDialog(self.main, params_needed)
                self.main.wait_window(dialog.popup)
                params = dialog.params
                del dialog  # we don't need it any more, created per-query
                # If we close the window early (X out of it), don't run the query
                if len(params) != len(params_needed):
                    # Check if the MAIN window was closed while the params dialog was open
                    try:
                        self.enable_buttons()
                        return
                    except:
                        print("[!] Main window was closed! Exiting...")
                        exit(0)
            print("[*] params = " + str(params))
            cursor.execute(query_dict[query_num][2](params))
            column_names = cursor.column_names
            returned_rows = [row for row in cursor]
            self.populate_results_table(column_names, returned_rows)
            print("[+] " + str(column_names))
            print("[+] " + str(returned_rows) + "\n")
            self.enable_buttons()

    def run_custom_query(self):
        self.disable_buttons()
        query_window = QueryDialog(self.main)
        self.main.wait_window(query_window.popup)
        query: str = query_window.query.get()
        del query_window  # we don't need it any more, created per-query
        print("[*] query = " + query)
        # If we close the window early (X out of it), don't run the query
        if not query:
            # Check if the MAIN window was closed while the params dialog was open
            try:
                self.enable_buttons()
                return
            except:
                print("[!] Main window was closed! Exiting...")
                exit(0)
        try:
            cursor.execute(query)
            column_names = cursor.column_names
            returned_rows = [row for row in cursor]
            self.populate_results_table(column_names, returned_rows)
            # Hide error if visible
            if self.error_label.winfo_viewable():
                self.error_label.pack_forget()
            print("[+] " + str(column_names))
            print("[+] " + str(returned_rows) + "\n")
        except mysql.connector.errors.ProgrammingError:
            # Show error if not already visible
            self.error_label["text"] = self.error_custom_syntax
            if not self.error_label.winfo_viewable():
                # Show error
                self.error_label.pack()
        self.enable_buttons()

    def populate_results_table(
        self, column_names: Tuple[str, ...], returned_rows: List[Tuple[str, ...]]
    ):
        # Clear table rows before inserting new ones
        self.results_table.delete(*self.results_table.get_children())

        # Set columns
        self.results_table["columns"] = column_names

        # Create column formats and column headings
        for col_name in column_names:
            self.results_table.column(col_name, anchor=W, width=100)
            self.results_table.heading(col_name, text=col_name, anchor=W)

        # Insert data
        # `parent` would be for nesting things, so we make it blank
        # `index="end"`` means "put it underneath of everything", building onto the list.
        # `iid` is a unique identifier
        # `text` is what goes in that phantom column, like the parent label (but we have no nesting/parents here)
        if returned_rows:
            for num, row in enumerate(returned_rows):
                self.results_table.insert(
                    parent="", index="end", iid=num, text=num + 1, values=row
                )

    def enable_buttons(self):
        self.execute_selected_button["state"] = "normal"
        self.execute_custom_button["state"] = "normal"

    def disable_buttons(self):
        self.execute_selected_button["state"] = "disabled"
        self.execute_custom_button["state"] = "disabled"


if __name__ == "__main__":
    # Configure window settings
    app.title("BCCC Database Interactions")

    # Connect to our database
    db.connect

    # Create the main window class
    main_window = App(app)

    # Start the program
    app.mainloop()
