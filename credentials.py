import os

def readcredentials(filename = "credentials.txt"):
    """
    Input read from textfile: e-mail, password and server.
    Objective: obtaining e-mail and password in order to use your e-mail
    Output: dictionary with e-mail, password and server.
    """
    credentials = {}

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'filename')

    with open (my_file, "r") as reader:
        for line in reader:
            credentials_list.append(line.rstrip())

    credentials["server"]: credentials_list[0]
    credentials["email"]: credentials_list[1]
    credentials["password"]: credentials_list[2]

    return credentials

####################################################################################################

def getcredentials_smtp(parameter = "imap.gmail.com"):
    """
    Input set by user: e-mail, password and server.
    Objective: obtaining e-mail and password in order to use your e-mail
    Output: dictionary with e-mail, password and server.
    """
    credentials = {}
    credentials["email"] = input ("Inserte correo electrónico:\n")
    print("Inserte contraseña: ")
    credentials["password"] = input("")
    print("Inserte servidor.")
    print('Si su correo es Gmail, puede dejar esto en blanco. La opción predeterminada será {0}.'.format(parameter))
    server = input("")
    if server == "": credentials["server"] = parameter
    else: credentials["server"] = server
    return credentials

####################################################################################################
