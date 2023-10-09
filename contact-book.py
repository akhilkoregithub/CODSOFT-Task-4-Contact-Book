from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import sqlite3

# Database where we will store all the data
connector = sqlite3.connect('contacts.db')
cursor = connector.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS CONTACT_BOOK (S_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NUMBER TEXT, ADDRESS TEXT)"
)

def submit_record():
    global name_strvar, email_strvar, phone_strvar, address_entry, contact_tree
    global cursor
    name, email, phone, address = name_strvar.get(), email_strvar.get(), phone_strvar.get(), address_entry.get(1.0, END)

    if name == '' or email == '' or phone == '' or address == '':
        mb.showerror('Error!', "Please fill all the fields!")
    else:
        cursor.execute(
            "INSERT INTO CONTACT_BOOK (NAME, EMAIL, PHONE_NUMBER, ADDRESS) VALUES (?,?,?,?)",
            (name, email, phone, address))
        connector.commit()
        mb.showinfo('Contact added', 'We have stored the contact successfully!')
        # Clear the entry widgets
        name_strvar.set('')
        email_strvar.set('')
        phone_strvar.set('')
        address_entry.delete(1.0, END)
        contact_tree.delete(*contact_tree.get_children())  # Clear the Treeview widget
        list_contacts()  # Call list_contacts after inserting a record

        
def list_contacts():
    listbox.delete(0, END)  # Clear the listbox
    curr = connector.execute('SELECT NAME FROM CONTACT_BOOK')
    fetch = curr.fetchall()

    for data in fetch:
        listbox.insert(END, data[0])  # Append the name to the listbox

def delete_record():
    global contact_tree, cursor, connector

    # Get the selected item from the Treeview widget
    selected_item = contact_tree.selection()

    if not selected_item:
        mb.showerror("No item selected", "You have not selected any item!")
    else:
        values = contact_tree.item(selected_item, 'values')
        name = values[0]

        cursor.execute('DELETE FROM CONTACT_BOOK WHERE NAME = ?', (name,))
        connector.commit()

        mb.showinfo('Contact deleted', 'The desired contact has been deleted')

        # Refresh the Treeview widget
        contact_tree.delete(selected_item)


def view_record():
    selected_item = contact_tree.selection()
    if not selected_item:
        mb.showerror("No item selected", "You have not selected any item!")
    else:
        values = contact_tree.item(selected_item, 'values')
        name_strvar.set(values[0])
        email_strvar.set(values[1])
        phone_strvar.set(values[2])
        address_entry.delete(1.0, END)
        address_entry.insert(END, values[3])


def clear_fields():
    global name_strvar, phone_strvar, email_strvar, address_entry, contact_tree

    # Clear the selection in the Treeview widget
    contact_tree.selection_remove(contact_tree.selection())

    name_strvar.set('')
    phone_strvar.set('')
    email_strvar.set('')
    address_entry.delete(1.0, END)


def search():
    query = str(search_strvar.get())

    if query != '':
        contact_tree.delete(*contact_tree.get_children())  # Clear the Treeview widget
        curr = connector.execute('SELECT * FROM CONTACT_BOOK WHERE NAME LIKE ?', ('%' + query + '%',))
        check = curr.fetchall()

        for data in check:
            contact_tree.insert('', 'end', values=data[1:])  # Insert the data into the Treeview widget
            

def update_record():
    global name_strvar, email_strvar, phone_strvar, address_entry, contact_tree, cursor, connector
    
    # Get the selected item from the Treeview widget
    selected_item = contact_tree.selection()
    
    if not selected_item:
        mb.showerror("No item selected", "You have not selected any item!")
        return
    
    # Get the values of the selected record
    values = contact_tree.item(selected_item, 'values')
    
    # Get the updated values from the entry widgets
    updated_name = name_strvar.get()
    updated_email = email_strvar.get()
    updated_phone = phone_strvar.get()
    updated_address = address_entry.get("1.0", "end-1c")
    
    # Check if any of the fields are empty
    if updated_name == '' or updated_email == '' or updated_phone == '' or updated_address == '':
        mb.showerror('Error!', 'Please fill all the fields!')
        return

    # Update the record in the database
    cursor.execute(
        "UPDATE CONTACT_BOOK SET NAME=?, EMAIL=?, PHONE_NUMBER=?, ADDRESS=? WHERE NAME=?",
        (updated_name, updated_email, updated_phone, updated_address, values[0])
    )
    
    connector.commit()
    
    mb.showinfo('Contact updated', 'The contact has been updated successfully!')
    
    # Clear the entry widgets
    name_strvar.set('')
    email_strvar.set('')
    phone_strvar.set('')
    address_entry.delete(1.0, END)
    
    # Refresh the Treeview widget
    contact_tree.delete(*contact_tree.get_children())  # Clear the Treeview widget
    list_contacts()  # Call list_contacts after updating a record


# List saved contacts in the Treeview widget
def list_contacts():
    contact_tree.delete(*contact_tree.get_children())  # Clear existing entries
    curr = connector.execute('SELECT * FROM CONTACT_BOOK')
    for row in curr.fetchall():
        contact_tree.insert('', 'end', values=row[1:])


# GUI window
root = Tk()
root.title("Akhil Contact Book")
root.geometry('1200x550')
root.resizable(0, 0)

#  color and font variables
lf_bg = 'Gray70'  # Lightest Shade
cf_bg = 'Gray57'
rf_bg = 'Gray35'  # Darkest Shade
frame_font = ("Garamond", 14)

# StringVar variables
name_strvar = StringVar()
phone_strvar = StringVar()
email_strvar = StringVar()
search_strvar = StringVar()

# set frames components in the window
Label(root, text='CONTACT BOOK', font=("Noto Sans CJK TC", 15, "bold"), bg='Black', fg='White').pack(side=TOP, fill=X)

left_frame = Frame(root, bg=lf_bg)
left_frame.place(relx=0, relheight=1, y=30, relwidth=0.2)  

center_frame = Frame(root, bg=cf_bg)
center_frame.place(relx=0.2, relheight=1, y=30, relwidth=0.2)  

right_frame = Frame(root, bg=rf_bg)
right_frame.place(relx=0.4, relwidth=0.6, relheight=1, y=30) 

# components in the left frame
Label(left_frame, text='Name', bg=lf_bg, font=frame_font).place(relx=0.3, rely=0.05)

name_entry = Entry(left_frame, width=15, font=("Verdana", 11), textvariable=name_strvar)
name_entry.place(relx=0.1, rely=0.1)

Label(left_frame, text='Phone no.', bg=lf_bg, font=frame_font).place(relx=0.23, rely=0.2)

phone_entry = Entry(left_frame, width=15, font=("Verdana", 11), textvariable=phone_strvar)
phone_entry.place(relx=0.1, rely=0.25)

Label(left_frame, text='Email', bg=lf_bg, font=frame_font).place(relx=0.3, rely=0.35)

email_entry = Entry(left_frame, width=15, font=("Verdana", 11), textvariable=email_strvar)
email_entry.place(relx=0.1, rely=0.4)

Label(left_frame, text='Address', bg=lf_bg, font=frame_font).place(relx=0.28, rely=0.5)

address_entry = Text(left_frame, width=15, font=("Verdana", 11), height=5)
address_entry.place(relx=0.1, rely=0.55)

# components in the Middle Frame
search_entry = Entry(center_frame, width=18, font=("Verdana", 12), textvariable=search_strvar).place(relx=0.08, rely=0.06)

Button(center_frame, text='Search', font=frame_font, width=15, command=search).place(relx=0.13, rely=0.13)
Button(center_frame, text='Add Record', font=frame_font, width=15, command=submit_record).place(relx=0.13, rely=0.23)
Button(center_frame, text='View Record', font=frame_font, width=15, command=view_record).place(relx=0.13, rely=0.33)
Button(center_frame, text='Clear Fields', font=frame_font, width=15, command=clear_fields).place(relx=0.13, rely=0.43)
Button(center_frame, text='Delete Record', font=frame_font, width=15, command=delete_record).place(relx=0.13, rely=0.53)
Button(center_frame, text='Update Record', font=frame_font, width=15, command=update_record).place(relx=0.13, rely=0.63)

# components in the Right Frame
Label(right_frame, text='Saved Contacts', font=("Noto Sans CJK TC", 16), bg=rf_bg, fg='White').pack(pady=10)

#  Treeview widget for displaying the contacts in a table
columns = ("Name", "Email", "Phone Number", "Address")
contact_tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")

#  column headings
for col in columns:
    contact_tree.heading(col, text=col)
    contact_tree.column(col, width=150)  

#  Treeview widget
contact_tree.pack(expand=True, fill='both')

# List saved contacts initially
list_contacts()

# Finalizing the window
root.mainloop()
