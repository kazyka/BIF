from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()


class UploadPath(Base):
    __tablename__ = 'UploadPath'

    id = Column(Integer, primary_key=True)
    UploadDate = Column(DateTime(timezone=True))
    PdfName = Column(String)
    PathToFile = Column(String)
    CPR = Column(Integer)
    UserInitials = Column(String)
    OCRStartDate = Column(DateTime(timezone=True))
    OCREndDate = Column(DateTime(timezone=True))


class ProcessedData(Base):
    __tablename__ = 'ProcessedData'

    id = Column(Integer, primary_key=True)
    UniqueId = Column(Integer)
    Page = Column(Integer)
    Email = Column(String)
    PageMark = Column(Boolean)
    JournalType = Column(String)
    CreateData = Column(DateTime(timezone=True))
    DeleteData = Column(DateTime(timezone=True))
    # CPR = Column(Integer)
    Content = Column(String)
