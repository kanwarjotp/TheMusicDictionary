import json
from datetime import datetime

from TMDEngine import build
from TMDEngine import config


if __name__ == "__main__": # building the application for the first time, calling from cmd
    with open("app_params.json", "r") as params:
        app_info = json.load(params)
        
    if app_info["db_built"] == True:
        quit("Database already exists. Please check Config files for 'current_schema'")
    else: # create the database for the first time.
        build.build_app(first_build=True, schema_to_use=config.current_schema)
        new_app = json.dumps({
            "db_built": True,
            "date_built": str(datetime.now()),
            "db_used": config.current_schema
        }, indent=4) # creating JSON object to store information about the application
        with open("app_params.json", "w") as params:
            params.write(new_app)
        quit("Database {} built".format(config.current_schema))
        
        
    