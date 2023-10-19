# ----------------------------------------------------------------
# Author: Mihir Vadadoria, Adam Knott
# Date: 4/25/2023
#
# This program creates a class registration system.  It allows
# students to add courses, drop courses and list courses they are
# registered for. It also allows students to review the tuition
# costs for their course roster.
# -----------------------------------------------------------------
import tkinter as tk
import tkinter.messagebox as mb


from student import add_course, drop_course, list_courses
from billing import calculate_hours_and_bill, display_hours_and_bill
from Chatbot import main
import customtkinter as ctk


class MyGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.student_list = [('1001', '111'), ('1002', '222'),
                             ('1003', '333'), ('1004', '444')]
        self.student_in_state = {'1001': True,
                                 '1002': False,
                                 '1003': True,
                                 '1004': False}

        self.course_hours = {'CSC101': 3, 'CSC102': 4, 'CSC103': 5, 'CSC104': 3}
        self.course_roster = {'CSC101': ['1004', '1003'],
                              'CSC102': ['1001'],
                              'CSC103': ['1002'],
                              'CSC104': []}
        self.course_max_size = {'CSC101': 3, 'CSC102': 2, 'CSC103': 1, 'CSC104': 3}
        self.logged_in_student = None

        # MAIN WINDOW #
        self.main_window = tk.Tk()
        self.main_window.title('Student Registration')
        self.main_window.geometry('730x560')

        # ID AND PIN FRAME #
        self.id_pin_frame = tk.Frame(self.main_window)
        self.id_pin_frame.pack(side="top", fill="x")
        # ID
        self.id_label = tk.Label(self.id_pin_frame, text="ID: ")
        self.id_label.pack(side="left", padx=10, pady=10)
        self.id_entry = ctk.CTkEntry(self.id_pin_frame)
        self.id_entry.pack(side="left", padx=10, pady=10)
        # PIN
        self.pin_label = tk.Label(self.id_pin_frame, text="PIN: ")
        self.pin_label.pack(side="left", padx=10, pady=10)
        self.pin_entry = ctk.CTkEntry(self.id_pin_frame, show="*")
        self.pin_entry.pack(side="left", padx=10, pady=10)
        # LOGOUT BUTTON
        self.logout_button = ctk.CTkButton(self.id_pin_frame, text="Log Out", fg_color="#050980", command=self.logout)
        self.logout_button.pack(side="right", padx=10, pady=10)
        # LOGIN BUTTON
        self.login_button = ctk.CTkButton(self.id_pin_frame, text="Log In", fg_color="#050980", command=self.login)
        self.login_button.pack(side="right", padx=10, pady=10)

        # OPTIONS FRAME #
        self.options_frame = tk.Frame(self.main_window)
        self.options_frame.pack(side="top")
        # ADD COURSE
        self.add_course_button = ctk.CTkButton(self.options_frame, text="Add Course", fg_color="#050980", command=self.add_message)
        self.add_course_button.pack(side="left", padx=10, pady=10)
        # DROP COURSE
        self.drop_course_button = ctk.CTkButton(self.options_frame, text="Drop Course", fg_color="#050980", command=self.drop_message)
        self.drop_course_button.pack(side="left", padx=10, pady=10)
        # LIST COURSE
        self.list_courses_button = ctk.CTkButton(self.options_frame, text="List Courses", fg_color="#050980", command=self.list_courses)
        self.list_courses_button.pack(side="left", padx=10, pady=10)
        # SHOW BILL
        self.show_bill_button = ctk.CTkButton(self.options_frame, text="Show Bill", fg_color="#050980", command=self.show_bill)
        self.show_bill_button.pack(side="left", padx=10, pady=10)

        # OUTPUT FRAME #
        self.output_frame = tk.Frame(self.main_window)
        self.output_frame.pack(side="top", fill="both", expand=True)
        # OUTPUT TEXT
        self.output_text = ctk.CTkTextbox(self.output_frame, width=400, corner_radius=10, font=('Helvetica', 23))
        self.output_text.pack(side="top", fill="both", expand=True)

        # INPUT FRAME #
        self.input_frame = tk.Frame(self.main_window)
        self.input_frame.pack(side="top", fill="x")
        # INPUT TEXT
        self.input_text = ctk.CTkEntry(self.input_frame)
        self.input_text.pack(side="left", padx=10, pady=10)
        # ADD BUTTON
        self.add_button = ctk.CTkButton(self.input_frame, text="Add", state='disabled', fg_color="#050980", command=self.add_course)
        self.add_button.pack(side="left", padx=10, pady=10)
        # DROP BUTTON
        self.drop_button = ctk.CTkButton(self.input_frame, text="Drop", state='disabled', fg_color="#050980", command=self.drop_course)
        self.drop_button.pack(side="left", padx=10, pady=10)

        # CHAT AND EXIT BUTTONS
        self.end_frame = tk.Frame(self.main_window)
        self.end_frame.pack(side="bottom", anchor="se", padx=10, pady=10)
        self.exit_button = ctk.CTkButton(self.end_frame, text="Exit", fg_color="#050980", command=self.main_window.destroy)
        self.exit_button.pack(side="bottom")
        self.chat_button = ctk.CTkButton(self.end_frame, text="Questions? Ask Talon", fg_color="#050980", command=ChatBotGUI)
        self.chat_button.pack(side="bottom")

        tk.mainloop()

    def login(self):
        student_id = self.id_entry.get()
        pin = self.pin_entry.get()
        for id_, student_pin in self.student_list:
            if student_id == id_ and student_pin == pin:
                mb.showinfo("Success", "ID and PIN verified")
                self.logged_in_student = student_id
                return True
        mb.showerror("Error", "ID or PIN incorrect")
        return False

    def logout(self):
        self.id_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)
        self.input_text.delete(0, tk.END)
        self.add_button.configure(state='disabled')
        self.drop_button.configure(state='disabled')

    def add_message(self):
        if not self.check_login():
            return
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Enter course you want to add in below box and hit add")
        self.add_button.configure(state='normal')
        self.drop_button.configure(state='disabled')

    def drop_message(self):
        if not self.check_login():
            return
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Enter course you want to drop in below box and hit add")
        self.drop_button.configure(state='normal')
        self.add_button.configure(state='disabled')

    def add_course(self):
        course = self.input_text.get()
        student_id = self.id_entry.get()
        message = add_course(student_id, course, self.course_roster, self.course_max_size)
        self.output_text.insert(tk.END, f"\n{message}")
        self.output_text.see(tk.END)

    def drop_course(self):
        course = self.input_text.get()
        student_id = self.id_entry.get()
        message = drop_course(course, student_id, self.course_roster)
        self.output_text.insert(tk.END, f"\n{message}")
        self.output_text.see(tk.END)

    def list_courses(self):
        if not self.check_login():
            return
        student_id = self.id_entry.get()
        course, course_count = list_courses(student_id, self.course_roster)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f"Course registered: \n")
        self.output_text.insert(tk.END, "\n".join(course))
        self.output_text.insert(tk.END, f"\nTotal Number: {course_count}")

    def show_bill(self):
        if not self.check_login():
            return
        student_id = self.id_entry.get()
        hours, cost = calculate_hours_and_bill(student_id, self.student_in_state, self.course_roster, self.course_hours)
        display_hours_and_bill(hours, cost)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f"Course load: {hours} credit hours\n")
        self.output_text.insert(tk.END, f"Enrollment Cost: ${cost:.2f}")

    def check_login(self):
        student_id = self.id_entry.get()
        if student_id != self.logged_in_student:
            mb.showerror("Error", "Please log in first")
            return False
        return True


class ChatBotGUI:
    def __init__(self):
        self.chat_window = tk.Tk()
        self.chat_window.title("ChatBot")
        self.chat_window.geometry("400x500")

        self.chat_box = ctk.CTkTextbox(self.chat_window, width=400, border_color='black', font=('Helvetica', 18))
        self.chat_box.pack(fill='both', expand=True)

        self.input_box = ctk.CTkEntry(self.chat_window)
        self.input_box.pack(fill='x')
        self.chat_window.bind('<Return>', self.send_message)

        self.send_button = ctk.CTkButton(self.chat_window, text="Send", border_color='black', fg_color="#050980", command=self.send_message)
        self.send_button.pack(side='right')

        self.quit_button = ctk.CTkButton(self.chat_window, text="End Chat", border_color='black', fg_color="#050980", command=self.chat_window.destroy)
        self.quit_button.pack(side='left')

        tk.mainloop()

    def send_message(self, event=None):
        message = self.input_box.get()
        self.input_box.delete(0, 'end')
        self.display_message(f"You: {message}")
        response = main(message)
        self.display_message(f"Talon: {response}")

    def display_message(self, message):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.configure(state='disabled')
        self.chat_box.see('end')


my_gui = MyGUI()
