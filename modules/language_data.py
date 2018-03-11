from bson import ObjectId

from modules.db import Database


def get_language_by_id(arg):
    element = Database().get_languages().find_by_id(arg)
    element["classification"] = get_languages_classification_by_id(element["classification"])
    return element


def get_language_by_name(language):
    return Database().get_languages().find_one({'language': language})


def get_languages():
    Database().get_languages().find()


def get_languages_classification_by_id(classification_id):
    return Database().get_languages_classes().find_by_id(classification_id)


def get_languages_classification_parent(classification_id):
    element = get_languages_classification_by_id(classification_id)
    if element and element["parent"]:
        parent = get_languages_classification_by_id(element["parent"])
        return parent


def get_languages_classification_children(classification_id):
    return [get_languages_classification_by_id(child) for child in get_languages_classification_by_id(classification_id)["children"]]


def languages_classification_children_explore(classification_id):
    element = get_languages_classification_by_id(classification_id)
    for i in range(len(element["children"])):
        child_id = element["children"][i]
        child = languages_classification_children_explore(child_id)
        element["children"][i] = child
    return element


def connect(child_id, parent_id):
    database = Database().get_languages_classes()
    child = get_languages_classification_by_id(child_id)
    parent = get_languages_classification_by_id(parent_id)
    if child and parent:
        child["parent"] = parent["_id"]
        database.replace_by_id(child)
        if child_id not in parent["children"]:
            parent["children"].append(child_id)
        database.replace_by_id(parent)


def disconnect(child_id, parent_id):
    database = Database().get_languages_classes()
    child = get_languages_classification_by_id(child_id)
    parent = get_languages_classification_by_id(parent_id)
    child["parent"] = None
    parent["children"].remove(child_id)
    database.replace_by_id(child)
    database.replace_by_id(parent)


def post_languages_classification(classification):
    if "parent" not in classification:
        classification["parent"] = None
    if "children" not in classification:
        classification["children"] = []
    if "languages" not in classification:
        classification["languages"] = []
    Database().get_languages_classes().insert_one(classification)


def delete_languages_classification_by_id(_id):
    Database().get_languages_classes().delete_by_id(_id)


def get_languages_classifications_tree():
    roots = Database().get_languages_classes().find({"parent": None})
    for i in range(len(roots)):
        roots[i] = languages_classification_children_explore(roots[i])
    return roots

"""
european_id = "5aa30ffe488c96143003ad84"
slavic_id = "5aa30ffe488c96143003ad7d"
slavic_west_id = "5aa30ffe488c96143003ad78"
slavic_south_id = "5aa30ffe488c96143003ad79"
slavic_east_id = "5aa30ffe488c96143003ad77"
germanic_id = "5aa30ffe488c96143003ad80"
romance_id = "5aa30ffe488c96143003ad82"

delete_languages_classification_by_id(european_id)
delete_languages_classification_by_id(slavic_id)
delete_languages_classification_by_id(slavic_west_id)
delete_languages_classification_by_id(slavic_south_id)
delete_languages_classification_by_id(slavic_east_id)
delete_languages_classification_by_id(germanic_id)
delete_languages_classification_by_id(romance_id)

post_languages_classification({"classification": "european", "_id": ObjectId(european_id)})
post_languages_classification({"classification": "slavic", "_id": ObjectId(slavic_id)})
post_languages_classification({"classification": "slavic west", "_id": ObjectId(slavic_west_id)})
post_languages_classification({"classification": "slavic south", "_id": ObjectId(slavic_south_id)})
post_languages_classification({"classification": "slavic east", "_id": ObjectId(slavic_east_id)})
post_languages_classification({"classification": "germanic", "_id": ObjectId(germanic_id)})
post_languages_classification({"classification": "romance", "_id": ObjectId(romance_id)})

connect(slavic_west_id, slavic_id)
connect(slavic_south_id, slavic_id)
connect(slavic_east_id, slavic_id)
connect(slavic_id, european_id)
connect(germanic_id, european_id)
connect(romance_id, european_id)

test = "5aa30ffe488c96143003ad7d"
#print(languages_class_children_explore(european_id))


def printtree(branch=None):
    if branch is None:
        branch = get_languages_classifications_tree()[0]
        print("root: " + branch["classification"])
    leaves = branch["children"]
    if leaves:
        print("explore: " + branch["classification"])
        for leaf in leaves:
            printtree(leaf)
    else:
        print("end: " + branch["classification"])

printtree()
#delete_languages_class_by_id("5aa312b0488c961b60bc0307")
#delete_languages_class_by_id("5aa312b0488c961b60bc030a")
#delete_languages_class_by_id("5aa31308488c960968b25d94")
#delete_languages_class_by_id("5aa31308488c960968b25d97")
"""