from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Lab Slot Scheduler Backend - PRJ069")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for Lab Slot
class LabSlot(BaseModel):
    id: int
    lab_name: str
    date: str
    slot_time: str
    student_name: Optional[str] = None
    student_regno: Optional[str] = None
    status: str = "Available"

# In-memory database
lab_slots: List[LabSlot] = []

@app.get("/")
def home():
    return {
        "message": "Welcome to Lab Slot Scheduler Backend - PRJ069",
        "docs_url": "/docs",
        "endpoints": {
            "GET /slots": "Get all slots",
            "POST /slots": "Create new slot",
            "GET /slots/{id}": "Get single slot",
            "PUT /slots/{id}": "Book or Update slot",
            "DELETE /slots/{id}": "Delete slot"
        }
    }

@app.get("/slots", response_model=List[LabSlot])
def get_slots():
    return lab_slots

@app.post("/slots", response_model=LabSlot)
def create_slot(slot: LabSlot):
    for s in lab_slots:
        if s.id == slot.id:
            raise HTTPException(status_code=400, detail="Slot ID already exists")
    lab_slots.append(slot)
    return slot

@app.get("/slots/{slot_id}", response_model=LabSlot)
def get_slot(slot_id: int):
    for s in lab_slots:
        if s.id == slot_id:
            return s
    raise HTTPException(status_code=404, detail="Slot not found")

@app.put("/slots/{slot_id}", response_model=LabSlot)
def update_slot(slot_id: int, updated: LabSlot):
    for i, s in enumerate(lab_slots):
        if s.id == slot_id:
            lab_slots[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Slot not found")

@app.delete("/slots/{slot_id}")
def delete_slot(slot_id: int):
    for i, s in enumerate(lab_slots):
        if s.id == slot_id:
            del lab_slots[i]
            return {"message": "Slot deleted successfully"}
    raise HTTPException(status_code=404, detail="Slot not found")