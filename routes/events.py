from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event, EventUpdate
from typing import List

from beanie import PydanticObjectId
from database.connection import Database


event_database = Database(Event)
event_router = APIRouter(tags=["Events"])

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events()-> List[Event]:
    events = await event_database.get_all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId)-> Event:
    event = await event_database.get(id)
    # for event in events:
    #     if event.id == id:
    #         return event
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with id not exists"
        )
    return event
    
@event_router.post("/new")
async def create_event(body: Event= Body(...))-> dict:
    #events.append(body)
    await event_database.save(body)
    return {
        "message":"Event created successfully"
    }

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate)-> Event:
    print(body)
    updated_event = await event_database.update(id,body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with id does not exists"
        )
    return updated_event
    
@event_router.delete("/{id}")
async def delete_event(id:PydanticObjectId)-> dict:
    event = await event_database.delete(id)
    if not event:               
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with id does not exists"
        )
    return {"message": "Event deleted succesfully"}
    # for event in events:
    #     if event.id == id:
    #         events.remove(event)


@event_router.delete("/")
async def delete_all_events()-> dict:
    events.clear()
    return{
        "message": "Events deleted successfully"
    }