from ..model import models, database

models.Base.metadata.create_all(bind=database.engine)