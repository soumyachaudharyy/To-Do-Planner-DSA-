import tkinter as tk
from tkinter import ttk, simpledialog

class Node:
    def __init__(self, priority, task): 
        self.priority = priority
        self.task = task
        self.is_done = False
        self.left = None
        self.right = None

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo App")

        self.tree = ttk.Treeview(self.root, columns=("Priority", "Task", "Status"), show="headings")
        self.tree.heading("Priority", text="Priority", command=lambda: self.sort_tree("Priority"))
        self.tree.heading("Task", text="Task", command=lambda: self.sort_tree("Task"))
        self.tree.heading("Status", text="Status", command=lambda: self.sort_tree("Status"))
        self.tree.pack(pady=10)

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_button.pack(pady=5)

        done_button = tk.Button(self.root, text="Mark Done", command=self.mark_done)
        done_button.pack(pady=5)

        delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_button.pack(pady=5)

        self.root_node = None
        self.load_sample_data()

    def add_task(self):
        priority = simpledialog.askinteger("Enter Priority", "Enter Priority:")
        task = simpledialog.askstring("Enter Task", "Enter Task:")
        if priority is not None and task:
            self.root_node = self.insert_task(self.root_node, priority, task)
            self.update_tree()

    def mark_done(self):
        priority = simpledialog.askinteger("Mark as Done", "Enter Priority to mark as done:")
        if priority is not None:
            node = self.search_by_priority(self.root_node, priority)
            if node:
                node.is_done = True
                self.update_tree()

    def delete_task(self):
        priority = simpledialog.askinteger("Delete Task", "Enter Priority to delete:")
        if priority is not None:
            self.root_node = self.delete_task_node(self.root_node, priority)
            self.update_tree()

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.display_tasks(self.root_node)

    def display_tasks(self, node):
        if node is not None:
            self.display_tasks(node.right)
            status = "Done" if node.is_done else "Not Done"
            self.tree.insert("", "end", values=(node.priority, node.task, status))
            self.display_tasks(node.left)

    def sort_tree(self, column):
        task_data = [(self.tree.set(child, "Priority"), self.tree.set(child, "Task"), self.tree.set(child, "Status"), child) for child in self.tree.get_children("")]
        
        if column == "Priority":
            task_data.sort(key=lambda x: int(x[0]))
        elif column == "Task":
            task_data.sort(key=lambda x: x[1])
        else:
            task_data.sort(key=lambda x: x[2])
        
        for i, item in enumerate(task_data):
            self.tree.move(item[3], "", i)

    def insert_task(self, node, priority, task):
        if node is None:
            return Node(priority, task)
        if priority < node.priority:
            node.left = self.insert_task(node.left, priority, task)
        elif priority > node.priority:
            node.right = self.insert_task(node.right, priority, task)
        return node

    def search_by_priority(self, node, priority):
        if node is None:
            return None
        if priority == node.priority:
            return node
        elif priority < node.priority:
            return self.search_by_priority(node.left, priority)
        else:
            return self.search_by_priority(node.right, priority)

    def delete_task_node(self, node, priority):
        if node is None:
            return node
        if priority < node.priority:
            node.left = self.delete_task_node(node.left, priority)
        elif priority > node.priority:
            node.right = self.delete_task_node(node.right, priority)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_larger_node = self.find_min(node.right)
            node.priority, node.task, node.is_done = min_larger_node.priority, min_larger_node.task, min_larger_node.is_done
            node.right = self.delete_task_node(node.right, min_larger_node.priority)
        return node

    def find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def load_sample_data(self):
        self.root_node = self.insert_task(self.root_node, 3, "Finish coding")
        self.root_node = self.insert_task(self.root_node, 1, "Study for exam")
        self.root_node = self.insert_task(self.root_node, 2, "Buy groceries")
        self.update_tree()

if __name__ == "__main__":
    app = ToDoApp(tk.Tk())
    app.root.mainloop()
