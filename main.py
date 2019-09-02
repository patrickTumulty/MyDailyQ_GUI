import tkinter as tk
import file_io as fio
from reminder import*


months = {}
months['January'] = 1
months['February'] = 2
months['March'] = 3
months['April'] = 4
months['May'] = 5
months['June'] = 6
months['July'] = 7
months['August'] = 8
months['September'] = 9
months['October'] = 10
months['November'] = 11
months['December'] = 12

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

years = [2019, 2020, 2021, 2022, 2023, 2024]


def Main():
    root = tk.Tk()
    root.title("My Daily Q")
    root.resizable(width=False, height=False)
    global app
    app = MainWindow(root)
    app.populate_list_pending()
    root.mainloop()

class MainWindow:
    def __init__(self, master):
        # ---- Variables ----
        self.root = master
        self.pending_assignments = None
        self.past_assignments = []
        self.main_font = 'Helvetica', 13

        # ---- Frames ----

        self.list_box_frame = tk.Frame(self.root)
        self.list_box_frame.grid(row=0, column=0)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=1)

        self.description_frame = tk.Frame(self.root)
        self.description_frame.grid(padx=10, pady=10, row=1, column=0, sticky='w')

        self.view_window = ViewReminderWindow(self.description_frame)

        # ---- ListBox ----

        self.lb_scrollbar = tk.Scrollbar(self.list_box_frame)
        self.lb_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lb_assignments = tk.Listbox(self.list_box_frame)
        self.lb_assignments.config(width=35, selectmode=tk.SINGLE)
        self.lb_assignments.bind('<<ListboxSelect>>', self.cursor_select)
        self.lb_assignments.pack()
       
        self.lb_assignments.config(yscrollcommand=self.lb_scrollbar.set)
        self.lb_scrollbar.config(command=self.lb_assignments.yview)

        # ---- Buttons ----

        self.b_Add = tk.Button(self.button_frame, text="Add+", width=10, command=self.open_add_reminder_window)
        self.b_Add.grid(row=0, column=0)

        self.b_Refresh = tk.Button(self.button_frame, text="Refresh", width=10, command=self.refresh_list)
        self.b_Refresh.grid(row=1, column=0)

        self.b_Quit = tk.Button(self.button_frame, text="Quit", width=10, command=self.save_and_exit)
        self.b_Quit.grid(row=2, column=0)
    
    def refresh_list(self):
        self.lb_assignments.delete(0, tk.END)
        fio.save('assignments', self.pending_assignments)
        self.populate_list_pending()

    def save_to_completed(self, new_item):
        self.past_assignments.append(new_item)
        fio.save('completed_assignments', self.past_assignments)

    def populate_list_pending(self):
        self.pending_assignments = fio.load('assignments')
        self.past_assignments = fio.load('completed_assignments')
        for item in self.pending_assignments:
            item.update_time_till_due()
        sorted_data = sort_assignments(self.pending_assignments)
        self.populate_list(sorted_data)

    def populate_list(self, data):
        for obj in data:
            formatted_string = self.format_string(obj.title, obj.time_till_due)
            self.lb_assignments.insert(tk.END, formatted_string)

    def format_string(self, title, time):
        if len(title) <= 40:
            for i in range(40 - len(title)):
                title += " "
            title += ': ({})'.format(time)
        elif len(title) > 40:
            title = title[0:35] + '...  : ({})'.format(time)
        return title
    
    def save_and_exit(self):
        fio.save('assignments', self.pending_assignments)
        fio.save('completed_assignments', self.past_assignments)
        self.root.destroy()
    
    def open_add_reminder_window(self):
        self.add_reminder_window = AddReminderWindow()
    
    def cursor_select(self, *args):
        val = self.lb_assignments.get(self.lb_assignments.curselection())
        selected_item_title = val.split(":")[0].strip()
        selected_obj = None
        for idx, obj in enumerate(self.pending_assignments):
            if obj.title == selected_item_title:
                selected_obj = self.pending_assignments[idx]
                break
        self.update_description(selected_obj)
    
    def update_description(self, obj):
        self.view_window.update_text(obj)

    def view_history(self):
        pass


class ViewReminderWindow:
    def __init__(self, master):
        self.root = master
        self.root.config(width=80)
        self.selected_item = None
        self.spawn = False
        self.b_completed = tk.Button(self.root, text="Completed", width=15, command=self.complete_item)
        self.b_delete = tk.Button(self.root, text="Delete", width=15, command=self.delete_item)

        self.l_label = tk.Label(self.root, text='Label: ', justify=tk.LEFT)
        self.l_dueDate = tk.Label(self.root, text='Due Date: ', justify=tk.LEFT)
        self.l_description = tk.Label(self.root, text='Description: ', justify=tk.LEFT)
        self.l_dateCreated = tk.Label(self.root, text='Date Created: ', justify=tk.LEFT)

        self.l_label_display = tk.Label(self.root, justify=tk.LEFT)
        self.l_dueDate_display = tk.Label(self.root, justify=tk.LEFT)
        self.l_description_display = tk.Label(self.root, justify=tk.LEFT, wraplength=160)
        self.l_dateCreated_display = tk.Label(self.root, justify=tk.LEFT)

    def update_text(self, obj):
        self.add_widgets()
        self.selected_item = obj
        self.l_label_display.config(text=obj.title)
        self.l_description_display.config(text=obj.description)
        self.l_dueDate_display.config(text=obj.due_date.date())
        self.l_dateCreated_display.config(text=obj.date_created.date())
        

    def add_widgets(self):
        if self.spawn == False:
            self.l_label.grid(row=0, column=0, sticky='nw')
            self.l_description.grid(row=1, column=0, sticky='nw')
            self.l_dueDate.grid(row=2, column=0, sticky='nw')
            self.l_dateCreated.grid(row=3, column=0, sticky='nw')

            self.l_label_display.grid(row=0, column=1, sticky='nw')
            self.l_description_display.grid(row=1, column=1, sticky='nw')
            self.l_dueDate_display.grid(row=2, column=1, sticky='nw')
            self.l_dateCreated_display.grid(row=3, column=1, sticky='nw')

            self.b_completed.grid(row=4, column=0)
            self.b_delete.grid(row=4, column=1)
            self.spawn = True
        else:
            pass

    def delete_item(self):
        app.pending_assignments.remove(self.selected_item)
        app.refresh_list()

    def complete_item(self):
        app.save_to_completed(self.selected_item)
        app.pending_assignments.remove(self.selected_item)
        app.refresh_list()

class AddReminderWindow:
    def __init__(self):
        app.b_Add.config(state=tk.DISABLED)
        self.add_window = tk.Tk()
        self.add_window.title("My Daily Q")

        self.add_frame = tk.Frame(self.add_window)
        self.add_frame.grid(row=0, columnspan=2, padx=10)

        self.date_frame = tk.Frame(self.add_frame)
        self.date_frame.grid(row=1, column=1)
        # ---- Variables ----

        self.selected_month = tk.StringVar(self.add_frame)
        self.selected_month.set('Month')

        self.selected_day = tk.StringVar(self.add_frame)
        self.selected_day.set('Day')

        self.selected_year = tk.StringVar(self.add_frame)
        self.selected_year.set('Year')

        # ---- Labels ----

        self.l_title = tk.Label(self.add_frame, text="Title:")
        self.l_title.grid(row=0, column=0, sticky='w')

        self.l_dueDate = tk.Label(self.add_frame, text="DueDate:")
        self.l_dueDate.grid(row=1, column=0, sticky='w')

        self.l_description = tk.Label(self.add_frame, text="Description:")
        self.l_description.grid(row=2, column=0, sticky='nw')

        # ---- Entry ----

        self.e_title = tk.Entry(self.add_frame, width=38, font=('Helvetica', 13))
        self.e_title.grid(row=0, column=1)

        self.e_month = tk.OptionMenu(self.date_frame, self.selected_month, *months)
        self.e_month.grid(row=0, column=0, padx=5)

        self.e_day = tk.OptionMenu(self.date_frame, self.selected_day, *days)
        self.e_day.grid(row=0, column=1, padx=5)

        self.e_year = tk.OptionMenu(self.date_frame, self.selected_year, *years)
        self.e_year.grid(row=0, column=2, padx=5)

        self.e_description = tk.Text(self.add_frame, width=35, height=8, bg="#F3F3F3", font=("Helvetica", 15))
        self.e_description.grid(row=2, column=1)

        self.b_Quit = tk.Button(self.add_window, text='Quit', width=10, command=self.quit_add_reminder_window)
        self.b_Quit.grid(row=1, column=0, sticky='e')

        self.b_Save_Reminder = tk.Button(self.add_window, text='Save', width=10, command=self.save_new_assignment)
        self.b_Save_Reminder.grid(row=1, column=1, sticky='w')

        self.add_window.mainloop()

    def retrieve_text(self):
        input_val = self.e_description.get('1.0', 'end-1c')
        return input_val

    def quit_add_reminder_window(self):
        app.b_Add.config(state=tk.NORMAL)
        self.add_window.destroy()

    def save_new_assignment(self):
        des = self.retrieve_text()
        title = self.e_title.get()
        obj = Assignment(title, des)
        input_day = int(self.selected_day.get())
        input_month = int(months[self.selected_month.get()])
        input_year = int(self.selected_year.get())
        obj.set_due_date(input_day, input_month, input_year)
        app.pending_assignments.append(obj)
        app.refresh_list()
        self.quit_add_reminder_window()        

if __name__ == "__main__":
    Main()




