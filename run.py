"""
This allows you to run app in three different flavour(Environment)
each with its own level of verbosity

    usage
            `export APP_SETTINGS="testing"`
            `export SECRET="OwnDarkSecret"`
            # where APP_SETTINGS can be testing, production or development

"""
import os
from app import create_app

app_config = os.getenv('APP_SETTINGS')
app = create_app(app_config)

if __name__ == "__main__":
    app.run()
