from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Sheet(Base):
    __tablename__ = 'sheets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    music_id = Column(Integer, ForeignKey('music.id', ondelete='CASCADE'))
    sheet_name = Column(String(255))
    sheet_img = Column(String)

    music = relationship('Music', back_populates='sheets')

    @classmethod
    def create_sheet(cls, session, music_id, sheet_name, sheet_path):
        sheet_img = Base.read_file_as_string(sheet_path)
        new_sheet = cls(music_id=music_id, sheet_name=sheet_name, sheet_img=sheet_img)
        session.add(new_sheet)
        session.commit()