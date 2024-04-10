import uvicorn

from configs.app import get_application

# not remove this import because this file is
# being used as a module on alembic's env.py
from dependencies.sql_alchemy_base import Base

# For migrations propouses, we need to import the Base class from here
AlembicBase = Base

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
