import datetime
import calendar
import file_io as fio

class Note:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.date_created = datetime.datetime.now()
        
class Assignment(Note):
    def __init__(self, title, description, completion=False):
        super().__init__(title, description)
        self.completion_status = completion
        self.due_date = None
        self.time_till_due = None

    def set_due_date(self,day, month, year, time="11:58:PM"):
        """
        day: int

        month: int

        year: int

        time: string : format example ["11:59:PM"]
            note: Only enter time if the due date requires a specific time of day
        """
        if time == "11:59:PM":
            self.due_date = datetime.datetime(year, month, day)
        else:
            time = time.split(":")
            time[0] = int(time[0]) # hours 
            time[1] = int(time[1]) # minutes
            if time[2] == "AM":
                if time[0] == 12:
                    time[0] -= 12
                else:
                    pass
            elif time[2] == "PM":
                if time[0] == 12:
                    pass
                else:
                    time[0] += 12
            self.due_date = datetime.datetime(year, month, day, time[0], time[1])
    
    def update_time_till_due(self):
        """
        This function will update the self.time_till_due parameter with a string
        representing the time from now till the due date.

        """
        td = (self.due_date.date() - datetime.datetime.now().date()).days
        if td == 0:
            time = str(self.due_date - datetime.datetime.now())
            time = time.split(':')
            if time[0] == "1":
                self.time_till_due = "{} Hour".format(time[0])
            elif time[0] == "0":
                self.time_till_due = "{} Minutes".format(time[1])
            else:
                self.time_till_due = "{} Hours".format(time[0])
        elif td == 1:
            self.time_till_due = "{} Day".format(td)
        elif td > 1:
            self.time_till_due = "{} Days".format(td)
        elif td < 0:
            self.time_till_due = "Past Due"


def get_month_range(year, month):
    if month == 12:
        number_of_days = datetime.date(year + 1, 1, 1) - datetime.date(year, month, 1)
    else:
        number_of_days = datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)
    return number_of_days.days



def sort_assignments(assignments):
    """
    assignments: list of assignment objects

    sorts assignments based on time_till_due parameter

    """
    def _custom_sort(t):
        return t[1]
    days_list = []
    hours_list = []
    minutes_list = []
    over_due_list = []
    obj_list = []
    for idx, obj in enumerate(assignments):
        num = (obj.time_till_due).split(" ")
        if num[1] == "Day" or num[1] == "Days":
            days_list.append((idx, int(num[0])))
        elif num[1] == "Hour" or num[1] == "Hours":
            hours_list.append((idx, int(num[0])))
        elif num[1] == "Minutes":
            minutes_list.append((idx, int(num[0])))
        elif num[1] == "Due":
            over_due_list.append(idx)
    days_list.sort(key=_custom_sort)
    hours_list.sort(key=_custom_sort)
    minutes_list.sort(key=_custom_sort)
    if len(over_due_list) == 0:
        pass
    else:
        for idx in over_due_list:
            obj_list.append(assignments[idx])
    if len(minutes_list) == 0:
        pass
    else:
        for idx, num in minutes_list:
            obj_list.append(assignments[idx])
    if len(hours_list) == 0:
        pass
    else:
        for idx, num in hours_list:
            obj_list.append(assignments[idx])
    if len(days_list) == 0:
        pass
    else:
        for idx, num in days_list:
            obj_list.append(assignments[idx])
    return obj_list
    

# l = sort_assignments(events)
# for item in l:
#     print(item.time_till_due)


# a = Assignment("Event 1", "Description")
# a.set_due_date(13,9,2019)
# a.update_time_till_due()
# # print(a.time_till_due)

# b = Assignment("Event 2", "Description")
# b.set_due_date(7,9,2019)
# b.update_time_till_due()
# # print(b.time_till_due)

# c = Assignment("Event 3", "Description")
# c.set_due_date(28,8,2019)
# c.update_time_till_due()
# # print(c.time_till_due)

# d = Assignment("Event 3", "Description")
# d.set_due_date(26,8,2019)
# d.update_time_till_due()
# # print(d.time_till_due)

# events = [a, b, c, d]

# # fio.save("assignments", events)

# a = fio.load('assignments')
# for item in a:
#     print(item.title)


