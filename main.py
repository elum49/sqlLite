import sqlite3
import tkinter as tk
import os

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Студенты")
        self.root.geometry("500x300")

        if os.path.exists('students.db'):
            os.remove('students.db')
        
        self.conn = sqlite3.connect('students.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                grade INTEGER
            )
        ''')
        self.conn.commit()
        
        tk.Label(root, text="Имя:").pack()
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.pack()
        
        tk.Label(root, text="Оценка:").pack()
        self.grade_entry = tk.Entry(root, width=30)
        self.grade_entry.pack()
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Добавить", command=self.add).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Удалить", command=self.delete).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Изменить", command=self.edit).pack(side=tk.LEFT, padx=5)
    
        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.show()
    
    def add(self):
        name = self.name_entry.get().strip()
        grade = self.grade_entry.get().strip()
        
        if name and grade:
            grade_int = int(grade)
            self.cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade_int))
            self.conn.commit()
            self.name_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
            self.show()
                
    
    def delete(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            student_id = self.student_ids[index]
            self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.conn.commit()
            self.show()
    
    def show(self):
        self.listbox.delete(0, tk.END)
        self.student_ids = []
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()
        for row in rows:
            self.listbox.insert(tk.END, f"{row[1]} - оценка: {row[2]}")
            self.student_ids.append(row[0])
            
    def edit(self):
        selected = self.listbox.curselection()
        if not selected:
            print("Выберите студента для изменения")
            return
        
        index = selected[0]
        student_id = self.student_ids[index]
        self.cursor.execute("SELECT name, grade FROM students WHERE id = ?", (student_id,))
        student_data = self.cursor.fetchone()
        if student_data:
            current_name, current_grade = student_data
            
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Редактирование студента")
            edit_window.geometry("300x200")
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            tk.Label(edit_window, text="Имя:").pack(pady=5)
            name_entry = tk.Entry(edit_window, width=30)
            name_entry.pack(pady=5)
            name_entry.insert(0, current_name)
            
            tk.Label(edit_window, text="Оценка:").pack(pady=5)
            grade_entry = tk.Entry(edit_window, width=30)
            grade_entry.pack(pady=5)
            grade_entry.insert(0, str(current_grade))
            
            def save_changes():
                new_name = name_entry.get().strip()
                new_grade = grade_entry.get().strip()
                
                if new_name and new_grade:
                    new_grade_int = int(new_grade)
                    self.cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?",(new_name, new_grade_int, student_id))
                    self.conn.commit()
                    self.show()
                    edit_window.destroy()

            button_frame = tk.Frame(edit_window)
            button_frame.pack(pady=10)
            
            tk.Button(button_frame, text="Сохранить", command=save_changes).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Отмена", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
