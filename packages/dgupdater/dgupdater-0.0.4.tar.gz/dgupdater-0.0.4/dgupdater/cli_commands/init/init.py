from click import command, echo, option
from json import dump
from .func.check_mongo_string import check_mongo_string

arguments = {
    'name': {
        'prompt': "Name of the Application: ",
        'help': "The name of the Application. It should be unique for every app "
    },
    'version': {
        'prompt': "Version of the Application: ",
        'help': "The version of the Application."
    },
    'mongodb_connection_string': {
        'prompt': "MongoDB Connection String: ",
        'help': "The MongoDB Connection String for a cloud cloud cluster."
    },
    
}
dgupdaterconf_json = {
    "app_name": "",
    "version": "",
    "mongodb_connection_string": "",
    "files": {}
}

@command()
@option("--name", "-n", required = True, prompt = arguments["name"]["prompt"], help = arguments["name"]["help"])
@option("--version", "-v", required = True, prompt = arguments["version"]["prompt"], help = arguments["version"]["help"])    
@option("--mongodbstr", "-m", callback = check_mongo_string, required = True, prompt = arguments["mongodb_connection_string"]["prompt"], help = arguments["mongodb_connection_string"]["help"])
def init(name, version, mongodbstr):
    # print(name, version, mongodbstr)
    echo("\n\nInitializing this directory for autoupdation...")

    dgupdaterconf_json["app_name"] = name
    dgupdaterconf_json["version"] = version
    # dgupdaterconf_json["mongodb_connection_string"] = mongodbstr
    dgupdaterconf_json["mongodb_connection_string"] = mongodbstr




    with open("dgupdaterconf.json", "w") as f:
        dump(dgupdaterconf_json, f, indent = 4)
        

