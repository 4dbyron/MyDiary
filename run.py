"""
This allows you to run app in three different flavour(Environment)
each with its own level of verbosity
app__init__.py
"""

import os
from auth import create_app

app_name = os.getenv("APP_SETTINGS")
app = create_app(config_name=app_name)

if __name__ == "__main__":
    app.run()
