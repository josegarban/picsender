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
    pprint.pprint(compressed)


    # Convert the nested dictionary into a list containing dictionaries
    people = []
    for record in compressed.keys():
        person = dict()
        person["attachments"] = compressed[record]["filepath"]
        # Comment the line below for testing
        person["email"] = [compressed[record]["Correo"]]
        # Uncomment the line below for testing
        # person["email"] = ["example@example.com"]
        person["gender"] = compressed[record]["Sexo"]
        try: # Get first first name only
            person["firstname"] = compressed[record]["Nombres"].split(" ")[0]
        except:
            person["firstname"] = compressed[record]["Nombres"]
        person["lastname"] = compressed[record]["Apellidos"]
        people.append(person)

    # Send an e-mail per recipient
    for person in people:
        flaskmailer(person)
        print("Sending", people.index(person)+1, "out of", str(len(people))+"...")
        pprint.pprint(person)

    return None

if __name__ == '__main__':
    main()
