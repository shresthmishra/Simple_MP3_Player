import tkinter as tk
root = tk.Tk()
count = 0
label = tk.Label(root, text=f"Count: {count}")
label.pack()
def increment():
    global count
    count += 1
    label.config(text=f"Count: {count}")
button = tk.Button(root, text="Increment", command=increment)
button.pack()
root.mainloop()