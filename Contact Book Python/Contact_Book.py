#Import Required Modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import sqlite3
#Functions
#Open my Website in Browser
def openWebsite(url):
    webbrowser.open_new(url)
#Select any Contact from Treeview
def selectContact(e):
    SN_entry.delete(0, END) #Clears SN_entry Box
    name_entry.delete(0, END) #Clears name_entry Box
    num_entry.delete(0, END) #Clears num_entry Box
    email_entry.delete(0, END) #Clears email_entry Box
    selected = my_tree.focus() #Selects the Contacts Focused in Treeview
    values=my_tree.item(selected, 'values') #Define values variables with the list Selected
    SN_entry.insert(0, values[0]) #Inserts SN value in SN Entry Box
    name_entry.insert(0, values[1]) #Inserts Name value in Name Entry Box
    num_entry.insert(0, values[2]) #Inserts Number value in Number Entry Box
    email_entry.insert(0, values[3]) #Inserts Email value in Email Entry Box
#Refresh the Treeview
def refreshDB():
    connect = sqlite3.connect("Contact_List.db") #Connects to the DataBase
    cursor = connect.cursor() #Creates a cursor in DataBase
    cursor.execute("SELECT rowid, * FROM contacts") #Selects rowid and all other columns from the database
    contactLists = cursor.fetchall() #Fectches all selected items to contactLists variable
    global count #Defines Global variable count
    count = 0 #Initializes Count to zero
    for record in contactLists: #for one item in selections
        if count%2 == 0: #If the row is even
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[2], record[3], record[4]), tags=('evenrow',)) #Edit the row inforations from the database
        else: #If the row is odd
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[2], record[3], record[4]), tags=('oddrow',)) #Edit the row inforations from the database
        count += 1 #Increase the value of variable count by 1
    connect.commit() #Commit the changes in DataBase
    connect.close() #Closes the Connection to the DataBase
#Updates the Contacts with new values
def updateContact():
    selected=my_tree.focus() #Selects the Contacts Focused in Treeview
    my_tree.item(selected, text="", values=(SN_entry.get(),name_entry.get(), num_entry.get(), email_entry.get())) #Define values variables with the list Selected and from the Entry Boxes
    connect = sqlite3.connect("Contact_List.db") #Connects to the DataBase
    cursor = connect.cursor() #Creates a cursor in DataBase
    cursor.execute("""UPDATE contacts SET
    SN=:SN,
    name=:Name,
    number=:Number,
    email=:Email
    WHERE oid=:oid""",
    {
    'SN' : SN_entry.get(), #Updates SN Column with value from SN_entry Box
    'Name' : name_entry.get(), #Updates Name Column with value from name_entry Box
    'Number' : num_entry.get(), #Updates Number Column with value from num_entry Box
    'Email' : email_entry.get(), #Updates Email Column with value from email_entry Box
    'oid' : SN_entry.get() #Updates Rowid with value from SN_entry Box
    }) #Executes the Changes
    connect.commit() #Commit the changes in DataBase
    connect.close() #Closes the Connection to the DataBase
    #Clear Entry Boxes
    name_entry.delete(0, END) #Clears name_entry Box
    num_entry.delete(0, END) #Clears num_entry Box
    email_entry.delete(0, END) #Clears email_entry Box
#Add new Contacts
def addContact():
    connect = sqlite3.connect("Contact_List.db") #Connects to the DataBase
    cursor = connect.cursor() #Creates a cursor in DataBase
    cursor.execute("INSERT INTO contacts VALUES (:SN, :Name, :Number, :Email)",{
    'SN' : SN_entry.get(), #Adds to the SN column the data from SN_entry Box
    'Name' : name_entry.get(), #Adds to the Name column the data from name_entry Box
    'Number' : num_entry.get(), #Adds to the Number column the data from num_entry Box
    'Email' : email_entry.get() #Adds to the Email column the data from email_entry Box
    }) #Executes the Changes
    connect.commit() #Commit the changes in DataBase
    connect.close() #Closes the Connection to the DataBase
    #Clear Entry Boxes
    SN_entry.delete(0,END) #Clears SN_entry Box
    name_entry.delete(0, END) #Clears name_entry Box
    num_entry.delete(0, END) #Clears num_entry Box
    email_entry.delete(0, END) #Clears email_entry Box
    my_tree.delete(*my_tree.get_children()) #Clears the Treeview
    refreshDB() #Refreses the Treeview with added data
#Delete one or many selected Contacts
def deleteContact():
    warning = messagebox.askyesno("Delete!!!", "Are you sure you want to delete all selected contacts?") #Asks for the Confirmation to delete Contacts
    if warning == 1: #If the user choose yes
        selections=my_tree.selection() #Selects the Contacts Focused in Treeview
        deleteRowId = [] #Defines an empty list
        for contact in selections: #for one item in selections
            deleteRowId.append(my_tree.item(contact, 'values')[0]) #Appends the Defined list with rowid numbers
            my_tree.delete(contact) #Deletes the contact from Treeview
            connect = sqlite3.connect("Contact_List.db") #Connects to the DataBase
            cursor = connect.cursor() #Creates a cursor in DataBase
            cursor.executemany("DELETE FROM contacts WHERE oid=?",deleteRowId) #Deletes the selected contact from Database
            connect.commit() #Commit the changes in DataBase
            connect.close() #Closes the Connection to the DataBase
        messagebox.showinfo("Deleted!", "The Contacts Selected were deleted.") #Messagebox to inform that all slected contacts have been deleted
        SN_entry.delete(0,END) #Clears SN_entry Box
        name_entry.delete(0, END) #Clears name_entry Box
        num_entry.delete(0, END) #Clears num_entry Box
        email_entry.delete(0, END) #Clears email_entry Box
#Clear the Database Table and Delete All Contacts at Once
def clearAll():
    warning = messagebox.askyesno("Delete!!!", "Are you sure you want to delete all contacts?") #Asks for the Confirmation to delete Contacts
    if warning == 1:  #If the user choose yes
        for contact in my_tree.get_children(): #for one item in selections
            my_tree.delete(contact) #Clears all rows from the Treeview
        connect = sqlite3.connect("Contact_List.db") #Connects to the DataBase
        cursor = connect.cursor() #Creates a cursor in DataBase
        cursor.execute("DROP TABLE contacts") #Deletes the Table from DataBase
        connect.commit() #Commit the changes in DataBase
        connect.close() #Closes the Connection to the DataBase
        messagebox.showinfo("Deleted!", "All Contacts got deleted.") #Messagebox to inform that all contacts have been deleted
        SN_entry.delete(0,END) #Clears SN_entry Box
        name_entry.delete(0, END) #Clears name_entry Box
        num_entry.delete(0, END) #Clears num_entry Box
        email_entry.delete(0, END) #Clears email_entry Box
        connect = sqlite3.connect("Contact_List.db") #Again Connects to the DataBase
        cursor = connect.cursor() #Creates a cursor in DataBase
        cursor.execute("""CREATE TABLE if not exists contacts(
        SN integer, name text, number integer, email text)""") #Recreates a new empty table, this is needed to use add contact button without restarting the program
        connect.commit() #Commit the changes in DataBase
        connect.close() #Closes the Connection to the DataBase
#Start Connection to DataBase on Start of Program
connect = sqlite3.connect("Contact_List.db") #Connects to the DataBase
cursor = connect.cursor() #Creates a cursor in DataBase
cursor.execute("""CREATE TABLE if not exists contacts(
SN integer, name text, number integer, email text)""") #Executes the changes in the database and creates an empty table
connect.commit() #Commit the changes in DataBase
connect.close() #Closes the Connection to the DataBase
#Now for the GUI Design
#Creates Window
root = Tk() #Initializes Tkinter
root.title("Contacts") #Gives a title to the Window
root.geometry("750x580") #Sets the Geometry Size of Window
root.iconbitmap('Brand-Logo-Icon.ico') #Icon for the Window
root.resizable(False, False) #Restricts user to resize the Window
root.configure(bg='lemon chiffon') #Background Color dor Window
appLabel = Label(root, text="Contact Address Book", font=("Times", "42", "bold italic"), fg="red", bg='lemon chiffon', anchor=CENTER) #Label for Appname
appLabel.pack() #Packs appLabel
appLabel.place(x=10,y=5) #Position for appLabel
#STYLE TREEVIEW
style = ttk.Style() #Executes tkinter style for Treeview
style.theme_use('default') #Sets the Treeview Theme to deefault
style.configure('Treeview', background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3", font=("Helvetica", "12", "")) #Configures the background color, rowheight and fieldbackground color to custom
style.configure('Treeview.Heading', background='lightblue',font=("Helvetica", "12", ""))
style.map('Treeview', background=[('selected','#347083')]) #Sets Custom color for selected row
#TREEVIEW FRAME
tree_frame = Frame(root) #Creates a frame for Treeview
tree_frame.pack() #Packs the Treeview Frame
tree_frame.place(x=50, y=75) #Position for tree_frame
tree_scroll = Scrollbar(tree_frame) #Creates a scrollbar in tree_frame
tree_scroll.pack(side=RIGHT, fill=Y) #Position for the Scrollbar
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended") #Creates the Treeview inside tree_frame
tree_scroll.config(command=my_tree.yview) # Sets the command for Scrollbar
my_tree['columns']=("SN","name","number","email") #Creates the table in Treeview
my_tree.column("#0", width=0, stretch=NO) #Hides the default Column
my_tree.column("SN", width=50, anchor=W, minwidth=15) #Creates a SN Column
my_tree.column("name", width=225, anchor=W, minwidth=25) #Creates a Name Column
my_tree.column("number", anchor=CENTER, width=150, minwidth=25) #Creates a Number Column
my_tree.column("email", anchor=W, width=225, minwidth=25) #Creates an Email Column
my_tree.heading("SN", text="S.N.", anchor=W) #Defines the Heading for SN column to S.N.
my_tree.heading("name", text="Contact's Name", anchor=W) #Defines the Heading for name column to Contact's Name
my_tree.heading("number", text="Contact Number", anchor=W) #Defines the Heading for number column to Contact Number
my_tree.heading("email", text="Email", anchor=W) #Defines the Heading for email column to Email
my_tree.tag_configure('oddrow', background='white') #Sets the background for oddrows to white
my_tree.tag_configure('evenrow', background='tomato') #Sets the background for evenrows to orangered
my_tree.pack() #Packs the Treeview
#ENTRYBOX FRAME
entry_frame = LabelFrame(root, text="Contact", background="lemon chiffon", bd=4, fg='red', labelanchor=N) #Creates a frame for Entry Boxes
SN_label = Label(entry_frame, text="Unique Id") #Creates SN_label
SN_label.grid(row=0, column=0, padx=10, pady=10) #Position for Hiding SN_label
SN_entry = Entry(entry_frame) #Creates SN_entry
SN_entry.grid(row=0, column=1, padx=10, pady=10) #Position for Hiding SN_entry
name_label = Label(entry_frame, text="Contact's Name", background="lemon chiffon") #Creates name_label
name_label.grid(row=0, column=0, padx=10, pady=10) #Position for name_label
name_entry = Entry(entry_frame) #Creates name_entry
name_entry.grid(row=0, column=1, padx=10, pady=10) #Position for name_entry
num_label = Label(entry_frame, text="Number", background="lemon chiffon") #Creates num_label
num_label.grid(row=0, column=2, padx=10, pady=10) #Position for num_label
num_entry = Entry(entry_frame) #Creates num_entry
num_entry.grid(row=0, column=3, padx=10, pady=10) #Position for num_entry
email_label = Label(entry_frame, text="Email", background="lemon chiffon") #Creates email_label
email_label.grid(row=0, column=4, padx=10, pady=10) #Position for email_label
email_entry = Entry(entry_frame) #Creates email_entry
email_entry.grid(row=0, column=5, padx=10, pady=10) #Position for email_entry
entry_frame.pack() #Packs Data Frame
entry_frame.place(x=40, y=365) #Positions entry_frame
#BUTTON FRAME
button_frame = LabelFrame(root, text="Buttons", background="lemon chiffon", bd=4, fg='red', labelanchor=N) #Creates a frame for Buttons
add_button = Button(button_frame, text="Add Contact", fg='white', bg='red', font=("Helvetica", "11", "italic"), bd='3', command=addContact) #Creates Add Contact Button
add_button.grid(row=0, column=0, padx=10, pady=5) #Position add_button
update_button = Button(button_frame, text="Update Contact", fg='white', bg='red', font=("Helvetica", "11", "italic"), bd='3', command=updateContact) #Creates Update Contact Button
update_button.grid(row=0, column=1, padx=10, pady=5) #Position update_button
delete_button = Button(button_frame, text="Delete Contacts", fg='white', bg='red', font=("Helvetica", "11", "italic"), bd='3', command=deleteContact) #Creates Delete Contact Button
delete_button.grid(row=0, column=2, padx=10, pady=5) #Position delete_button
clearAll_button = Button(button_frame, text="Clear Contact Book", fg='white', bg='red', font=("Helvetica", "11", "italic"), bd='3', command=clearAll) #Creates Delete All Button
clearAll_button.grid(row=0, column=3, padx=10, pady=5) #Position clearAll_button
button_frame.pack() #Packs Button Frame
button_frame.place(x=100, y=435) #Position for Button Frame
my_tree.bind("<ButtonRelease-1>", selectContact) #Method to select contcts on clicking a row and input its values to respective entry boxes
#DEVELOPER LABEL
devNameLabel = Label(root, text="Developed By:", font=("Times", "20", "underline"), fg="green", bg="lemon chiffon")
devNameLabel.pack()
devNameLabel.place(x=225, y=500)
devName = Label(root, text="Raunak Kumar", font=("Times", "20"), fg="orange", bg="lemon chiffon")
devName.pack()
devName.place(x=400, y=500)
devContact = Label(root, text="Lets Connect", fg="blue", cursor="hand2")
devContact.pack()
devContact.place(x=350, y=540)
devContact.bind("<Button-1>", lambda e: openWebsite("https://www.raunakmishra.com.np/#Contact"))
refreshDB()
root.mainloop() #Executes window
