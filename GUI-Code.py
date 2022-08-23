import sqlite3
from tkinter import *
from tkinter.filedialog import askopenfile
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import csv

#Initiate Graphic User Interface
root = Tk()
root.title('Materialdatenbank')
#root.iconbitmap('C:/Users/natal/Documents/Erneuerbare Energie/Master Projekt/Datenbank/TH_Koeln_Logo.ico')
root.geometry("400x600")


# Create a database or connect to existing one
connection = sqlite3.connect('Materialien.db')
# Create a cursor
c = connection.cursor()

#Create table
c.execute("""CREATE TABLE IF NOT EXISTS Materialien(
        Name text,
        Hersteller text,
        ID text,
        Messwert integer)""")
    
# Create Table
c.execute("""CREATE TABLE IF NOT EXISTS Messwerte(
            MeasurementID integer,
            Frequency real)""")

measurements_df = None
fds_results_df = None

# Create function to select CSV-file from Windows Explorer
def add_csv():
 
    #Chose File to open
    file = askopenfile(mode='r', filetypes=[("csv files", "*.csv")])
    if not file:
            return None
    print(file.name)
 
    measurements_df = createDataFrameWith('MEASUREMENTS', file.name)
    fds_results_df = createDataFrameWith('FDS RESULTS', file.name)
    print(measurements_df.info())
    print(fds_results_df.info())
        
 
 
# Read CSV-File into dataframe ###################################################

def createDataFrameWith(measurement, path_to_csv):
    with open(path_to_csv, 'r', newline='', encoding='utf-8') as csvfile:
      rawCsv = csv.reader(csvfile, delimiter=';')
      
      readIndex = -1
      dataArray = []
      for i, row in enumerate(rawCsv):
        isReadingData = len(dataArray) != 0
        isEmptyRow = len(row) == 0

        keyWord = '[' + str(measurement) + ']'
        isAtKeyWord = not isReadingData and not isEmptyRow and row[0] == keyWord

        if isAtKeyWord:
            ## init readIndex
            readIndex = i +1

        isAtEndOfData = isReadingData and isEmptyRow
        if isAtEndOfData:
          break

        if readIndex == i:
          dataArray.append(row)
          readIndex = readIndex + 1
          
    headers = dataArray[:1][0]
    print(headers)
    data = dataArray[1:]

    return pd.DataFrame(data = data, columns=headers) 
    
# Create delete-Function for Database
def delete():
    # Create a database or connect to existing one
    connection = sqlite3.connect('Materialien.db')
    # Create a cursor
    c = connection.cursor()
    
    c.execute("DELETE from Materialien WHERE oid= " + delete_box.get())
   
    # Commit changes
    connection.commit()
    # Close connection
    connection.close()
    
    
# Create Update Function for Database
def edit():
    
    # Create a database or connect to existing one
    connection = sqlite3.connect('Materialien.db')
    # Create a cursor
    c = connection.cursor()
    
    editor = Tk()
    editor.title('Eintrag bearbeiten')
    editor.iconbitmap('C:/Users/natal/Documents/Erneuerbare Energie/Master Projekt/Datenbank/TH_Koeln_Logo.ico')
    editor.geometry("400x200")
    
   
    #Display Database
    record_ID = delete_box.get() #Eingegebene Nummer des zu ändernden Eintrags
    
    c.execute("SELECT * FROM Materialien WHERE oid= " + record_ID) #oid = zugewiesene ID innerhalb der Datenbank
    records = c.fetchall()
        
    #Eingabeboxen für neues Fenster
    Name_editor = Entry(editor, width=30)
    Name_editor.grid(row=0, column=1, padx=20, pady=(10,0))

    Hersteller_editor = Entry(editor, width=30)
    Hersteller_editor.grid(row=1, column=1)

    ID_editor = Entry(editor, width=30)
    ID_editor.grid(row=2, column=1)

    Messwert_editor = Entry(editor, width=30)
    Messwert_editor.grid(row=3, column=1)
    
    #Label für die Eingabeboxen im neuen Fenster
    Name_label_editor = Label(editor, text="Name")
    Name_label_editor.grid(row=0, column=0, pady=(10,0))

    Hersteller_label_editor = Label(editor, text="Hersteller")
    Hersteller_label_editor.grid(row=1, column=0)

    ID_label_editor = Label(editor, text="ID")
    ID_label_editor.grid(row=2, column=0)

    Messwert_label_editor = Label(editor, text="Messwert")
    Messwert_label_editor.grid(row=3, column=0)
    
    #Loop thru existing results and fill boxes with them
    for record in records:
        Name_editor.insert(0, record[0])
        Hersteller_editor.insert(0, record[1])
        ID_editor.insert(0, record[2])
        Messwert_editor.insert(0, record[3])
    
    #Create a Save-Button for Updates
    #save_button = Button(root, text="Änderungen speichern", command=save)
    #save_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)



# Create Submit Function for Database
def submit():
    # Create a database or connect to existing one
    connection = sqlite3.connect('Materialien.db')
    # Create a cursor
    c = connection.cursor()
    
    #Insert into Table
    c.execute("INSERT INTO Materialien VALUES(:Name, :Hersteller, :ID, :Messwert)",
              {
                  'Name': Name.get(),
                  'Hersteller': Hersteller.get(),
                  'ID': ID.get(),
                  'Messwert': Messwert.get()
              })

    # Commit changes
    connection.commit()
    # Close connection
    connection.close()
    

    # Clear Text Boxes
    Name.delete(0, END)
    Hersteller.delete(0, END)
    ID.delete(0, END)
    Messwert.delete(0, END)

    
#Create Display Function
def display():
    # Create a database or connect to existing one
    connection = sqlite3.connect('Materialien.db')
    # Create a cursor
    c = connection.cursor()
    
    #Display Database
    c.execute("SELECT *, oid FROM Materialien") #oid = zugewiesene ID innerhalb der Datenbank
    records = c.fetchall() #records = Datenbankeinträge
    #print(records) Schreibt Einträge nicht in die GUI, sondern in die Console
    
    #Loop durch Einträge
    print_records = ''
    for record in records: #records[0] würde nur den ersten Eintrag zeigen
        print_records += str(record) + "\n"   #str Datenbankeinträge in String konvertieren
                                                #str(record[0]) wäre nur der Name, [1] Hersteller usw.
    display_label = Label(root, text= print_records)
    display_label.grid(row=11, column=0, columnspan=2)
    
    
    # Commit changes
    connection.commit()
    # Close connection
    connection.close()





# Create Text Boxes 
Name = Entry(root, width=30)
Name.grid(row=0, column=1, padx=20, pady=(10,0))

Hersteller = Entry(root, width=30)
Hersteller.grid(row=1, column=1)

ID = Entry(root, width=30)
ID.grid(row=2, column=1)

Messwert = Entry(root, width=30)
Messwert.grid(row=3, column=1)

delete_box = Entry(root, width=10)
delete_box.grid(row=7, column=1)


# Create Text Box Labels
Name_label = Label(root, text="Name")
Name_label.grid(row=0, column=0, pady=(10,0))

Hersteller_label = Label(root, text="Hersteller")
Hersteller_label.grid(row=1, column=0)

ID_label = Label(root, text="ID")
ID_label.grid(row=2, column=0)

Messwert_label = Label(root, text="Messwert")
Messwert_label.grid(row=3, column=0)

delete_box_label = Label(root, text="Eintrag an Position")
delete_box_label.grid(row=7, column=0)




# Create Submit Button
submit_button = Button(root, text="Zur Datenbank hinzufügen", command=submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


# Create Display Button
display_button = Button(root, text="Datenbankeinträge anzeigen", command=display)
display_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create Delete Button
delete_button = Button(root, text="Eintrag löschen", command=delete)
delete_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create Update Button
update_button = Button(root, text="Eintrag bearbeiten", command=edit)
update_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create Add-CSV-Data Button
add_csv_button = Button(root, text="CSV-Datei einlesen", command=add_csv)
add_csv_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)



# Commit changes
connection.commit()

# Close connection
connection.close()

root.mainloop()