# Let's import the tools we need, like getting ingredients before baking a cake!
from fastapi import FastAPI  # FastAPI = a tool to build a web server (like a restaurant)
from fastapi.middleware.cors import CORSMiddleware  # This helps different websites talk to each other safely
from sqlalchemy import create_engine, Column, Integer, String, DateTime  # SQLAlchemy = tool for storing data in a filing cabinet
from sqlalchemy.ext.declarative import declarative_base  # This helps us describe what our data looks like
from sqlalchemy.orm import sessionmaker  # This helps us talk to the database (the filing cabinet)
from pydantic import BaseModel  # This checks that we get the right type of information
from datetime import datetime  # This helps us work with dates and times
import os  # This helps us work with the computer's files and folders

# Where do we want to store our data? Like choosing a filing cabinet!
DATABASE_URL = "sqlite:///./journal.db"

# Open the filing cabinet and get ready to use it
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This describes what each journal entry should look like
# Think of it like a template or form that everyone fills out the same way!
class Entry(Base):
    __tablename__ = "entries"  # The name of our filing cabinet drawer
    id = Column(Integer, primary_key=True, index=True)  # Each entry gets a special number (like a receipt)
    date = Column(String, index=True)  # What day did the student write this?
    appreciation = Column(String)  # What did they appreciate today? (the happy part!)
    negative = Column(String)  # What challenged them today? (the tough part)
    created_at = Column(DateTime, default=datetime.utcnow)  # When was this entry created?

# Actually create the filing cabinet drawer in our computer
Base.metadata.create_all(bind=engine)

# Create the web server (like opening a restaurant)
app = FastAPI()

# CORS = "Cross-Origin Resource Sharing" = Allow other websites to order from our restaurant
# This is like saying: "Anyone can call us and we'll serve them!"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # * means "everyone is allowed"
    allow_credentials=True,  # Allow them to send cookies
    allow_methods=["*"],  # Allow all types of requests (GET, POST, etc.)
    allow_headers=["*"],  # Allow any information in the request
)

# This describes what information we need to CREATE a new entry
# Like a recipe that shows what ingredients you must add
class EntryCreate(BaseModel):
    appreciation: str  # A sentence about something they appreciated
    negative: str  # A sentence about something that was challenging

# This describes what information we SEND BACK when you ask for an entry
# Like describing what a finished cake looks like when you ask for it
class EntryResponse(BaseModel):
    id: int  # The receipt number
    date: str  # The date
    appreciation: str  # The happy part
    negative: str  # The tough part

    class Config:
        from_attributes = True  # This lets us convert database stuff to this format

# ========== RESTAURANT MENU (ENDPOINTS) ==========
# These are like the menu items you can order from our restaurant!

# ENDPOINT 1: Save a new journal entry (when a student writes something new)
@app.post("/save", response_model=EntryResponse)
def save_entry(entry: EntryCreate):
    """
    POST /save = Save a new entry (like putting a new note in the filing cabinet)
    The student sends: appreciation and negative thoughts
    The server sends back: the entry with its new receipt number
    """
    db = SessionLocal()  # Open the filing cabinet
    today = datetime.now().strftime("%Y-%m-%d")  # Get today's date
    db_entry = Entry(date=today, appreciation=entry.appreciation, negative=entry.negative)  # Create a new entry
    db.add(db_entry)  # Put it in the filing cabinet
    db.commit()  # Save it permanently (like stamping it with approval!)
    db.refresh(db_entry)  # Get the fresh copy with the receipt number
    db.close()  # Close the filing cabinet
    return db_entry  # Send it back to the student

# ENDPOINT 2: Get all journal entries (when student wants to read all their past entries)
@app.get("/entries", response_model=list[EntryResponse])
def get_entries():
    """
    GET /entries = Get all entries from the filing cabinet
    The server sends back: a list of all saved entries (newest first!)
    """
    db = SessionLocal()  # Open the filing cabinet
    entries = db.query(Entry).order_by(Entry.id.desc()).all()  # Get all entries (newest first because .desc())
    db.close()  # Close the filing cabinet
    return entries  # Send the list back to the student

# ENDPOINT 3: Check if the server is alive (like a heartbeat check)
@app.get("/health")
def health():
    """
    GET /health = Is the server working?
    The server sends back: {"status": "ok"} = "Yes, I'm alive and ready to help!"
    """
    return {"status": "ok"}
