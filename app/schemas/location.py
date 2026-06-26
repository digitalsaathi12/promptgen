from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LocationSearchRequest(BaseModel):
    country: str = Field(..., example="India")
    state: str = Field(..., example="Madhya Pradesh")
    city: str = Field(..., example="Indore")
    area: str = Field(..., example="Vijay Nagar")
    category: str = Field(..., example="dentist", description="OSM POI category amenity (e.g. dentist, hospital, cafe)")
    radius: Optional[int] = Field(1000, description="Search radius in meters")
    limit: Optional[int] = Field(5, description="Limit count of results returned")

class CoordinateModel(BaseModel):
    lat: str
    lon: str

class CompetitorModel(BaseModel):
    business_name: str
    address: str
    rating: float
    coordinates: CoordinateModel

class LocationSearchResponse(BaseModel):
    business_name: str
    phone: Optional[str] = None
    website: Optional[str] = None
    address: str
    gmaps_link: str
    coordinates: CoordinateModel
    rating: float
    nearby_competitors: List[CompetitorModel] = []
