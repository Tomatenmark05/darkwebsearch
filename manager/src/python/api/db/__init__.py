from api.db import models
from api.db import database

models.Base.metadata.create_all(bind=database.engine)
