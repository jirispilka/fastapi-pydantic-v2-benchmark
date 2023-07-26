# generated by datamodel-codegen:
#   filename:  data_1mb.json
#   timestamp: 2022-11-15T14:10:15+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel
import orjson


class Customer(BaseModel):
    customer_id: str
    mobile: str
    name: str
    email: Any = None
    created_at: str = None
    updated_at: str = None
    dob: Optional[Any] = None


class ReadableBookingWithId(BaseModel):
    text: str
    post_back: str


class Booking(BaseModel):
    booking_id: str
    customer_id: str = None
    resource_id: str = None
    service_id: str = None
    service_name: Optional[str] = None
    date: str
    start_time: str
    end_time: str = None
    readable_booking: str
    created_at: str = None
    updated_at: str = None
    num_of_customers: Any = None
    status: str
    readable_booking_with_id: Optional[ReadableBookingWithId] = None


class Service(BaseModel):
    service_id: str
    name: str
    created_at: str
    updated_at: str


class MondayItem(BaseModel):
    start: str
    end: str


class TuesdayItem(BaseModel):
    start: str
    end: str


class WednesdayItem(BaseModel):
    start: str
    end: str


class ThursdayItem(BaseModel):
    start: str
    end: str


class FridayItem(BaseModel):
    start: str
    end: str


class SaturdayItem(BaseModel):
    start: str
    end: str


class SundayItem(BaseModel):
    start: str
    end: str


class AvailabilityCalendar(BaseModel):
    Monday: List[MondayItem]
    Tuesday: List[TuesdayItem]
    Wednesday: List[WednesdayItem]
    Thursday: List[ThursdayItem]
    Friday: List[FridayItem]
    saturday: List[SaturdayItem]
    Sunday: List[SundayItem]


class Resource(BaseModel):
    resource_id: str
    name: str
    capability: List[str]
    availability_calendar: AvailabilityCalendar
    OOO: Dict[str, Any]


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BusinessModel(BaseModel):
    _id: str
    business_name: str = None
    created_at: str = None
    updated_at: str = None
    customers: List[Customer] = None
    bookings: List[Booking] = None
    services: List[Service] = None
    resources: List[Resource] = None
