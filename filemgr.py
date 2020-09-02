import pprint, os, shutil
from PIL import Image
import dbhandler, dbchild, picsender, structures

MY_INSTRUCTION = """select child.Carnet, child.Nombres, child.Apellidos, child.Fotos, Blobtable.filepath
from child
inner join Blobtable on Blobtable.searchterm = child.Fotos
"""
MY_FILE = "output.sqlite"

def get_people_list():
    """
    Obtain list with people information and their associated pictures
    """
    # Perform custom query to get the information we need about the recipients
    instruction = "playinstruction.txt"
    file = "playfilename.txt"

    query = picsender.custom_query(MY_INSTRUCTION, MY_FILE)
    compressed = structures.compress_dictlist (query, "filepath", "Fotos")

    # Convert the nested dictionary into a list containing dictionaries
    people = []
    for record in compressed.keys():
        person = dict()
        person["uni_id"] = compressed[record]["Carnet"]
        person["attachments"] = compressed[record]["filepath"]
        person["firstnames"] = compressed[record]["Nombres"]
        person["lastnames"] = compressed[record]["Apellidos"]
        person["pic_num"] = compressed[record]["Fotos"]
        people.append(person)

    people_count = len({x for x in [p["uni_id"] for p in people]})

    print("There are {0} people in the list.".format(people_count))
    return people

def get_used_pics(people_list):
    """
    From the list with people, get a list of the used pictures
    """
    attachment_count, i = 0, 0
    while i < len(people_list):
        x = len(people_list[i]["attachments"])
        attachment_count, i = attachment_count + x, i + 1
    print("There are {0} attachments belonging to a person in the people list.".format(attachment_count))
    return attachment_count

def renamer1(people_list):
    """
    Copy all pictures to a new folder and change their names and sizes to arrange per photo number
    """
    # Copy
    src_folder = "Fotos"
    dst_folder = src_folder + "_pareadas"
    shutil.copytree(src_folder, dst_folder)
    print("Copied files in {0} to {1}".format(src_folder, dst_folder))

    # Rename files
    for count, filename in enumerate(os.listdir(dst_folder)):
        src = dst_folder + "/" + filename
        # Get last three digits in picture name
        pic_num = (filename[:-4])[-3:]
        for p in people_list:
            if p["pic_num"] == pic_num:
                addition = "_" + p["uni_id"] + "_" + p["firstnames"] + "_" + p ["lastnames"]
                # Rename
                dst = filename[:-4] + addition + ".jpg"
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

def renamer2(people_list):
    """
    Copy all pictures to a new folder and change their names and sizes to arrange by id
    """
    # Copy
    src_folder = "Fotos"
    dst_folder = src_folder + "_rotuladas"
    shutil.copytree(src_folder, dst_folder)
    print("Copied files in {0} to {1}".format(src_folder, dst_folder))

    # Rename files
    for count, filename in enumerate(os.listdir(dst_folder)):
        src = dst_folder + "/" + filename
        # Get last three digits in picture name
        pic_num = (filename[:-4])[-3:]
        for p in people_list:
            if p["pic_num"] == pic_num:
                addition = p["uni_id"] + "_" + p["firstnames"] + "_" + p ["lastnames"] + "_"
                # Rename
                dst = addition + ".jpg"
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
    renamer1(people)
    renamer2(people)

if __name__ == '__main__':
    main()
