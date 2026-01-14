
from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.db.models import Links, Content, Tag

router = APIRouter()


class LinkCreate(BaseModel):
	url: str


class LinkUpdate(BaseModel):
	url: Optional[str] = None
	analysed_on: Optional[date] = None


class LinkOut(BaseModel):
	id: int
	url: str
	analysed_on: Optional[date] = None

	class Config:
		orm_mode = True


@router.post("/", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
def create_link(payload: LinkCreate, db: Session = Depends(get_db)):
	existing = db.query(Links).filter(Links.url == payload.url).first()
	if existing:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Link already exists")

	link = Links(url=payload.url)
	db.add(link)
	db.commit()
	db.refresh(link)
	return link


@router.get("/", response_model=List[LinkOut])
def list_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	q = db.query(Links).offset(skip).limit(limit).all()
	return q


@router.get("/{link_id}", response_model=LinkOut)
def get_link(link_id: int, db: Session = Depends(get_db)):
	link = db.query(Links).filter(Links.id == link_id).first()
	if not link:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
	return link


@router.put("/{link_id}", response_model=LinkOut)
def update_link(link_id: int, payload: LinkUpdate, db: Session = Depends(get_db)):
	link = db.query(Links).filter(Links.id == link_id).first()
	if not link:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

	if payload.url is not None:
		link.url = payload.url
	if payload.analysed_on is not None:
		link.analysed_on = payload.analysed_on

	db.add(link)
	db.commit()
	db.refresh(link)
	return link


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, db: Session = Depends(get_db)):
	link = db.query(Links).filter(Links.id == link_id).first()
	if not link:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

	# Capture the URL so we can remove any Content rows that reference the same URL
	url = link.url

	# Delete Content rows that reference this URL. Use ORM delete to ensure relationship
	# cascade rules are applied (Content -> ContentTag will delete association rows).
	contents = db.query(Content).filter(Content.url == url).all()
	for c in contents:
		db.delete(c)

	# After removing contents, remove any Tag rows that no longer have associated content_links
	orphan_tags = db.query(Tag).filter(~Tag.content_links.any()).all()
	for t in orphan_tags:
		db.delete(t)

	# Finally remove the link itself
	db.delete(link)

	db.commit()
	return None



class LinkStatusOut(BaseModel):
	id: int
	url: str
	has_content: bool
	tags: List[str] = []


@router.get("/{link_id}/status", response_model=LinkStatusOut)
def link_status(link_id: int, db: Session = Depends(get_db)):
	"""Return whether the given link has an analysed Content entry and its tags."""
	link = db.query(Links).filter(Links.id == link_id).first()
	if not link:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

	content = db.query(Content).filter(Content.url == link.url).first()
	if not content:
		return LinkStatusOut(id=link.id, url=link.url, has_content=False, tags=[])

	tag_names = [t.name for t in content.tags]
	return LinkStatusOut(id=link.id, url=link.url, has_content=True, tags=tag_names)


