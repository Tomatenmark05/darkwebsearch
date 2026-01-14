from api.db import models
from api.db import database

models.Base.metadata.create_all(bind=database.engine)

def _seed_links():
	"""Insert two seed entries into the `links` table if they don't already exist."""
	session = database.SessionLocal()
	try:
		seed_urls = [
			"https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion"
		]
		for url in seed_urls:
			exists = session.query(models.Links).filter(models.Links.url == url).first()
			if not exists:
				session.add(models.Links(url=url))
		session.commit()
	except Exception as e:
		session.rollback()
		print(f"Error seeding links: {e}")
	finally:
		session.close()

# Run the seeding when this module is imported (keeps behavior similar to previous init-on-import)
_seed_links()

