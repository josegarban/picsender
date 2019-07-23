import sqlite3, pprint
import dbhandler, structures
from flaskmailer import flaskmailer

def custom_query (instruction,
                  sql_filename = "",
                  printinstructions = True):

    my_connector = dbhandler.create_connector(sql_filename)
    my_connector.row_factory = sqlite3.Row
    my_cursor    = my_connector.cursor()
    my_cursor.execute(instruction)
    result = [dict(row) for row in my_cursor.fetchall()]
    
    return result


MY_INSTRUCTION = """select child.Correo, child.Sexo, child.Nombres, child.Apellidos, Blobtable.filepath
from child
inner join Blobtable on Blobtable.searchterm = child.Fotos"""
MY_FILE = "output.sqlite"

def main ():
    
    # Perform custom query to get the information we need about the recipients
    instruction = "playinstruction.txt"
    file = "playfilename.txt"
    
    query = custom_query(MY_INSTRUCTION, MY_FILE)
    compressed = structures.compress_dictlist (query, "filepath", "Correo")
    
    # Convert the nested dictionary into a list containing dictionaries
    people = []
    for record in compressed.keys():
        person = {}
        person["attachments"] = compressed[record]["filepath"]
        person["email"] = [compressed[record]["Correo"]]
        person["gender"] = compressed[record]["Sexo"]
        try: # Get first first name only
            person["firstname"] = compressed[record]["Nombres"].split(" ")[0]
        except:
            person["firstname"] = compressed[record]["Nombres"]
        person["lastname"] = compressed[record]["Apellidos"]
        people.append(person)
        
    pprint.pprint(people)
    
    # Send an e-mail per recipient
    for person in people[0:]:
        flaskmailer(person)
        print(person)
    
    return None
    
if __name__ == '__main__':
    main()
