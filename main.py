import tkinter as tk
from tkinter import ttk, messagebox
import random, json, os
from datetime import datetime

class App:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Random Task Generator")
        self.win.geometry("550x450")
        
        self.tasks = [
            {"task": "Прочитать статью", "type": "учёба"},
            {"task": "Сделать зарядку", "type": "спорт"},
            {"task": "Пробежать 5 км", "type": "спорт"},
            {"task": "Решить 10 задач", "type": "учёба"},
            {"task": "Написать отчёт", "type": "работа"},
            {"task": "Посетить тренировку", "type": "спорт"},
            {"task": "Подготовиться к экзамену", "type": "учёба"},
            {"task": "Созвон с клиентом", "type": "работа"}
        ]
        self.history = self.load_json("history.json")
        self.init_ui()
    
    def load_json(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    return json.load(f)
        except: pass
        return []
    
    def save_json(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def init_ui(self):
        ttk.Label(self.win, text="Random Task Generator", 
                  font=("Arial", 14, "bold")).pack(pady=15)
        
        f1 = ttk.Frame(self.win)
        f1.pack(pady=10)
        ttk.Label(f1, text="Тип:").pack(side="left")
        self.filter = ttk.Combobox(f1, values=["Все", "учёба", "спорт", "работа"], 
                                   width=15, state="readonly")
        self.filter.set("Все")
        self.filter.pack(side="left", padx=5)
        
        ttk.Button(self.win, text="Сгенерировать", 
                   command=self.generate).pack(pady=5)
        self.result = ttk.Label(self.win, text="", font=("Arial", 11), 
                                wraplength=400)
        self.result.pack(pady=10)
        
        f2 = ttk.LabelFrame(self.win, text="Новая задача")
        f2.pack(pady=10, padx=20, fill="x")
        
        self.entry_task = ttk.Entry(f2, width=30)
        self.entry_task.pack(pady=5)
        self.entry_type = ttk.Entry(f2, width=30)
        self.entry_type.pack(pady=5)
        ttk.Button(f2, text="Добавить", 
                   command=self.add_task).pack(pady=5)
        
        ttk.Label(self.win, text="История:").pack()
        self.hist = tk.Text(self.win, height=12, width=60)
        self.hist.pack(pady=5, padx=20)
        self.update_hist()
    
    def generate(self):
        f = self.filter.get()
        tasks = self.tasks if f == "Все" else [t for t in self.tasks if t["type"] == f]
        
        if not tasks:
            messagebox.showwarning("Ошибка", f"Нет задач типа '{f}'")
            return
        
        task = random.choice(tasks)
        self.result.config(text=f"Задача: {task['task']}\nТип: {task['type']}")
        self.history.append({
            "task": task["task"], 
            "type": task["type"],
            "time": datetime.now().strftime("%d.%m.%Y %H:%M")
        })
        self.save_json("history.json", self.history)
        self.update_hist()
    
    def add_task(self):
        task = self.entry_task.get().strip()
        ttype = self.entry_type.get().strip()
        
        if not task or not ttype:
            messagebox.showerror("Ошибка", "Поля не могут быть пустыми!")
            return
        
        self.tasks.append({"task": task, "type": ttype})
        self.entry_task.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        messagebox.showinfo("Готово", f"Задача '{task}' добавлена")
    
    def update_hist(self):
        self.hist.delete(1.0, tk.END)
        if not self.history:
            self.hist.insert(1.0, "История пуста")
        else:
            for h in reversed(self.history[-15:]):
                self.hist.insert(tk.END, f"[{h['time']}] {h['task']} ({h['type']})\n")
    
    def run(self):
        self.win.mainloop()

if __name__ == "__main__":
App().run()
