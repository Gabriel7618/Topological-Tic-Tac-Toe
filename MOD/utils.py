class Stack:
    def __init__(self, length, data=None):
        self.length = length
        self.data = data
        if self.data == None:
            self.data = []

    def push(self, item):
        self.data.append(item)  # List Operations

    def pop(self):
        return self.data.pop()  # List Operations

    def peek(self):
        return self.data[-1]  # List Operations

    def full(self):
        if len(self.data) == self.length:  # List Operations
            return True
        return False

    def empty(self):
        if len(self.data) == 0:  # List Operations
            return True
        return False

    def index(self, index):
        return self.data[index]  # List Operations


def point_in_rect(point_x, point_y, rect_x, rect_y, rect_w, rect_h):
    if rect_x <= point_x <= rect_x + rect_w and rect_y <= point_y <= rect_y + rect_h:
        return True
    return False


def round_sf(value, sf):
    digits = 0
    temp_value = value
    while temp_value >= 1:
        temp_value //= 10
        digits += 1

    return round(value / 10**digits, sf) * 10**digits


def format_time(hour, minute):
    hour_string = str(hour) if hour >= 10 else f"0{hour}"
    minute_string = str(minute) if minute >= 10 else f"0{minute}"
    return f"{hour_string}:{minute_string}"
