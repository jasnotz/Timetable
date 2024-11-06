import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
import math
import pytz

KST = pytz.timezone('Asia/Seoul')

class TableAndClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8x3 Table & Clock")
        self.configure(bg="black")
        
        self.tb1_row_height = 60
        self.tb1_col_widths = [70, 70, 160]
        self.tb1_text_size = 14

        self.clock_number_size = 24

        self.tb2_row_height = 60
        self.tb2_col_width = 400
        self.tb2_text_size = 14
        self.row_data = [
            ["전자기기는 전원 반드시 끄고 제출하기"],
            ["본령 5분전에는 반드시 착석해 있기"],
            ["볼펜 사용 금지 & OMR 카드는 컴싸만 사용"],
            ["학교번호: "]
        ]

        self.create_ui()

    def create_ui(self):
        left_frame = tk.Frame(self, bg="black")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.create_table1(left_frame)

        right_frame = tk.Frame(self, bg="black")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.create_clock(right_frame)
        self.create_table2(right_frame)

        controls_frame = tk.Frame(self, bg="black")
        controls_frame.pack(fill="x", pady=5)
        self.create_controls(controls_frame)

    def create_table1(self, parent):
        table1_frame = tk.Frame(parent, bg="black")
        table1_frame.pack(fill="both", expand=True)
        
        self.table1_labels = []
        headers = ["구분", "과목", "시간"]
        rows = [
            ["1교시", "국어", "08:40~10:00 (80')"],
            ["2교시", "수학", "10:30~12:10 (100')"],
            ["점심", "", "12:10~13:00"],
            ["3교시", "영어", "13:10~14:20 (70')"],
            ["4교시", "한국사", "14:50~15:20 (30')"],
            ["4교시", "제1선택", "15:35~16:05 (30')"],
            ["4교시", "제2선택", "16:07~16:37 (30')"]
        ]
        
        for i, header in enumerate(headers):
            label = tk.Label(table1_frame, text=header, width=self.tb1_col_widths[i] // 10, 
                             font=("Arial", self.tb1_text_size), bg="black", fg="white")
            label.grid(row=0, column=i, padx=1, pady=1)
        
        for row_idx, row in enumerate(rows, start=1):
            row_labels = []
            for col_idx, cell in enumerate(row):
                label = tk.Label(table1_frame, text=cell, width=self.tb1_col_widths[col_idx] // 10, 
                                 font=("Arial", self.tb1_text_size), bg="black", fg="white")
                label.grid(row=row_idx, column=col_idx, padx=1, pady=1)
                label.bind("<Button-1>", lambda e, r=row_idx, c=col_idx: self.edit_table1(r, c))
                row_labels.append(label)
            self.table1_labels.append(row_labels)

    def edit_table1(self, row, col):
        current_text = self.table1_labels[row-1][col].cget("text")
        new_text = simpledialog.askstring("Edit", "Enter new value:", initialvalue=current_text)
        if new_text:
            self.table1_labels[row-1][col].config(text=new_text)

    def create_clock(self, parent):
        self.clock_canvas = tk.Canvas(parent, width=200, height=200, bg="black", highlightthickness=0)
        self.clock_canvas.pack(pady=10)
        self.update_clock()

    def update_clock(self):
        self.clock_canvas.delete("all")
        center_x, center_y = 100, 100
        radius = 90
        now = datetime.now(KST)
        
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.clock_canvas.create_text(x, y, text=str(i), fill="white", font=("Arial", self.clock_number_size))

        hour_angle = ((now.hour % 12) + now.minute / 60.0) * 30 - 90
        minute_angle = (now.minute + now.second / 60.0) * 6 - 90
        second_angle = now.second * 6 - 90
        
        self.draw_hand(center_x, center_y, radius * 0.5, hour_angle, 6)
        self.draw_hand(center_x, center_y, radius * 0.7, minute_angle, 4)
        self.draw_hand(center_x, center_y, radius * 0.9, second_angle, 2, "red")

        self.after(1000, self.update_clock)

    def draw_hand(self, x, y, length, angle, width, color="white"):
        end_x = x + length * math.cos(math.radians(angle))
        end_y = y + length * math.sin(math.radians(angle))
        self.clock_canvas.create_line(x, y, end_x, end_y, fill=color, width=width)

    def create_table2(self, parent):
        table2_frame = tk.Frame(parent, bg="black")
        table2_frame.pack(fill="both", expand=True)
        
        for row_idx, row in enumerate(self.row_data):
            label = tk.Label(table2_frame, text=row[0], width=self.tb2_col_width // 10, 
                             font=("Arial", self.tb2_text_size), bg="black", fg="white")
            label.grid(row=row_idx, column=0, padx=1, pady=1)
            label.bind("<Button-1>", lambda e, r=row_idx: self.edit_table2(r))

    def edit_table2(self, row):
        current_text = self.row_data[row][0]
        new_text = simpledialog.askstring("Edit", "Enter new value:", initialvalue=current_text)
        if new_text:
            self.row_data[row][0] = new_text
            self.create_table2(self)

    def create_controls(self, parent):
        tk.Button(parent, text="Add Row", command=self.add_row, bg="black", fg="white").pack(side="left", padx=5)
        tk.Button(parent, text="Remove Row", command=self.remove_row, bg="black", fg="white").pack(side="left", padx=5)

    def add_row(self):
        self.row_data.append(["여기를 눌러 공지를 추가하세요"])
        self.create_table2(self)

    def remove_row(self):
        if self.row_data:
            self.row_data.pop()
            self.create_table2(self)

app = TableAndClockApp()
app.mainloop()
