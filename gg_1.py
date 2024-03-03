import customtkinter as ctk
import tkinter as tk
from AutoCorrect import reccomand


global fulltext 
fulltext=""
def submit():
    global fulltext
    my_List.delete(0,ctk.END)
    text = entry.get()
    text = reccomand(text)
    entry.insert(ctk.END," ")
    entry.insert(ctk.END,text)
    my_List.insert(0,text)

app = ctk.CTk()
app.title("Recommendation System")
app.geometry("500x500")

my_label = ctk.CTkLabel(app, text="                Welcome !", font=("Helvetica ", 21))
my_label.place(relx=0.2, rely=0.1)


entry = ctk.CTkEntry(app, placeholder_text="Enter Your text", width=300)
entry.place(relx=0.2, rely=0.2)

my_List = ctk.CTkEntry(app, width=50 ,height=10,placeholder_text="recommanded")
my_List.pack(pady=200)

button = ctk.CTkButton(app,text="recommand",width=40,height=20,command=submit)
button.pack()

app.mainloop()
