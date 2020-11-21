from tkinter import *
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
results: List[Tuple[str, ...]] = []


def query1(params: Dict[str, str]) -> str:
    return '                                        \
        SELECT                                      \
            title                                   \
        FROM                                        \
            Course_christian                        \
        WHERE                                       \
            code IN (                               \
                SELECT                              \
                    course_code                     \
                FROM                                \
                    Program_Courses_christian       \
                WHERE                               \
                    program_id = (                  \
                        SELECT                      \
                            id                      \
                        FROM                        \
                            Program_christian       \
                        WHERE                       \
                            name = "{Program_name}" \
                    )                               \
            );                                      \
    '.format(**params)


def query2() -> str:
    print("Query 2!")


def query3():
    print("Query 3!")


def query4():
    print("Query 4!")


def query5():
    print("Query 5!")


def query6():
    print("Query 6!")


def query7():
    print("Query 7!")


def query8():
    print("Query 8!")


def query9():
    print("Query 9!")


def query10():
    print("Query 10!")


# List of all possible queries
# Description, Parameters needed, Query function
#
# If the attribute you need is, for example,'Program -> name', use the naming convention 'Program_name'
query_dict = {
    1:  ("List the names of the courses offered by a specific program.", ["Program_name"], query1),
    2:  ("List what courses are offered in a specific department during a specific semester.", query2),
    3:  ("List the first and last names of staff that teach a course in a specific program.", query3),
    4:  ("List the first and last names of staff that are also an advisor.", query4),
    5:  ("List the first and last names of students who have a specific staff member as an advisor.", query5),
    6:  ("Retrieve how many students withdrew/dropped a specific course during a specific semester.", query6),
    7:  ("Generate a list of professsors who have taught at Baltimore City Community College for >= five years as of a specific semester.", query7),
    8:  ("List all of the first and last names of students enrolled in a specific program who are female.", query8),
    9:  ("Find the name of the student who has a specific ID no.", query9),
    10: ("List the grade records of all of the courses during a specific semester for a particular student.", query10)
}


class Dialog:
    def __init__(self, main, params_needed: List[str]):
        popup = self.popup = Toplevel(main)
        popup.title("Enter parameters")

        params_box = self.params_box = Frame(popup, padx=10, pady=10)
        params_box.pack()

        self.params = {}
        for num, param_name in enumerate(params_needed):
            Label(params_box, anchor=W, text=param_name +
                  ":").grid(row=num, column=0)
            e = Entry(params_box)
            e.grid(row=num, column=1)
            self.params[param_name] = e

        button_frame = self.button_frame = Frame(popup, pady=10)
        button_frame.pack()
        Button(button_frame, text="Submit", command=self.pull_data_from_entries, font=("bold", 12),
               padx=10, pady=10).pack()

    def pull_data_from_entries(self) -> Dict[str, str]:
        for entry in self.params:
            self.params[entry] = self.params[entry].get()
        self.popup.destroy()


class App:
    def __init__(self, app):
        main = self.main = app
        # Define left and right halves
        left_frame = self.left_frame = Frame(main, padx=20)
        right_frame = self.right_frame = Frame(main, padx=20)
        left_frame.grid(row=0, column=0)
        right_frame.grid(row=0, column=1)

        title_frame = self.title_frame = Frame(left_frame, pady=10)
        title_frame.pack()
        Label(title_frame, text="Select your query below:",
              font=("bold", 12), pady=10).pack()

        # Frame for list of available queries
        query_list_frame = self.query_list_frame = LabelFrame(
            left_frame, text="Query list")
        query_list_frame.pack()

        query_num = self.query_num = IntVar(0)
        for i in range(1, len(query_dict)+1):
            Radiobutton(query_list_frame,
                        text=query_dict[i][0], variable=query_num, value=i).pack(anchor=W)

        execute_button_frame = self.execute_button_frame = Frame(
            left_frame, pady=10)
        execute_button_frame.pack()
        execute_button = self.execute_button = Button(execute_button_frame, text="Execute query",
                                                      font=("bold", 12), padx=10, pady=10, command=lambda: self.run_query(query_num.get()))
        execute_button.pack()

        # Right frame results list
        Label(
            right_frame, text="This is a test label that is a lot longer than the other text!").pack()
        Label(right_frame, text="This is where the results should show up, ideally with a scrollbar for long lists.").pack()

    # Currently only Query 1 works, which is checked for here.
    # Any other queries just print "Query X!"
    def run_query(self, query_num):
        if (query_num < 1):
            print("Please select a query")
        else:
            self.execute_button["state"] = "disabled"
            if (query_num == 1):
                cursor = db.cursor()
                params = []
                params_needed = query_dict[query_num][1]
                if (params_needed):
                    dialog = Dialog(self.main, params_needed)
                    self.main.wait_window(dialog.popup)
                    params = dialog.params
                    del dialog  # we don't need it any more, created per-query
                print("params = " + str(params))
                cursor.execute(query_dict[query_num][2](params))
                results.clear()
                for result in cursor:
                    results.append(result)
                print(results)
            else:
                query_dict[query_num][1]()
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
