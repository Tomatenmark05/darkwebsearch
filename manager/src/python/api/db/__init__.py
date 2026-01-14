from api.db import models
from api.db import database

models.Base.metadata.create_all(bind=database.engine)

def _seed_links():
	"""Insert two seed entries into the `links` table if they don't already exist."""
	session = database.SessionLocal()
	try:
		seed_urls = [
            "http://zkj7mzglnrbvu3elepazau7ol26cmq7acryvsqxvh4sreoydhzin7zid.onion",
            "http://cr32aykujaxqkfqyrjvt7lxovnadpgmghtb3y4g6jmx6oomr572kbuqd.onion",
            "http://f6wqhy6ii7metm45m4mg6yg76yytik5kxe6h7sestyvm6gnlcw3n4qad.onion",
            "http://zwf5i7hiwmffq2bl7euedg6y5ydzze3ljiyrjmm7o42vhe7ni56fm7qd.onion",
            "http://z7s2w5vruxbp2wzts3snxs24yggbtdcdj5kp2f6z5gimouyh3wiaf7id.onion"
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

