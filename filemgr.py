import pprint, os, shutil
from PIL import Image
import dbhandler, dbchild, picsender, structures

def get_people_list():
    """
    Obtain list with people information and their associated pictures
    """
    # Perform custom query to get the information we need about the recipients
    instruction = "playinstruction.txt"
    file = "playfilename.txt"

    query = picsender.custom_query(picsender.MY_INSTRUCTION, picsender.MY_FILE)
    compressed = structures.compress_dictlist (query, "filepath", "Correo")

    # Convert the nested dictionary into a list containing dictionaries
    people = []
    for record in compressed.keys():
        person = dict()
        person["attachments"] = compressed[record]["filepath"]
        person["email"] = [compressed[record]["Correo"]]
        person["gender"] = compressed[record]["Sexo"]
        person["firstnames"] = compressed[record]["Nombres"]
        person["lastnames"] = compressed[record]["Apellidos"]
        people.append(person)

    print("There are {0} people in the list.".format(len(people)))
    return people

def get_used_pics(people_list):
    """
    From the list with people, get a list of the used pictures
    """
    attachment_count, i = 0, 0
    while i < len(people_list):
        x = len(people_list[i]["attachments"])
        attachment_count, i = attachment_count + x, i + 1
    print("There are {0} attachments belonging to a person in the people dictionary.".format(attachment_count))
    return attachment_count

def renamer():
    """
    Copy all pictures to a new folder and change their names and sizes
    """
    # Copy
    src_folder = "Fotos"
    dst_folder = src_folder + "_copy"
    shutil.copytree(src_folder, dst_folder)
    print("Copied files in {0} to {1}".format(src_folder, dst_folder))

    # Rename files
    for count, filename in enumerate(os.listdir(dst_folder)):
        src = dst_folder + "/" + filename
        dst = filename[:-4] + "b" + ".jpg"
        dst = dst_folder + "/" + dst
        os.rename(src, dst)

    # Get file names
    filenames = [f for f in os.listdir(dst_folder) if os.path.isfile(os.path.join(dst_folder, f))]
    pprint.pprint(filenames)

    for count, filename in enumerate(os.listdir(dst_folder)):
        im = Image.open(dst_folder + "/" + filename)
        #image size
        size=(856,568)
        #resize image
        out = im.resize(size)
        #save resized image
        out.save(dst_folder + "/" + filename)

    return None

def main():
    people = get_people_list()
    get_used_pics(people)
    renamer()

if __name__ == '__main__':
    main()
