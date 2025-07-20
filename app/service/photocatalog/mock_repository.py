from pydantic import BaseModel
from typing import Iterator
import random

class TimestampModel(BaseModel):
    seconds: int
    nanos: int

class PhotoResponseModel(BaseModel):
    id: str
    description: str
    timestamp: TimestampModel
    content: str

class MockRepository:
    def __init__(self):
        self._photos = []

    def get_photo(self, id_: str) -> PhotoResponseModel | None:
        return next((photo for photo in self._photos if photo.id == id_), None)
    
    def add_photo(self, photo: PhotoResponseModel) -> PhotoResponseModel:
        self._photos.append(photo)
        return photo

    def get_random_photos(self, count: int) -> Iterator[PhotoResponseModel]:
        available_count = min(count, len(self._photos))
        
        if available_count == 0:
            return
        
        available_photos = self._photos.copy()
        
        random.shuffle(available_photos)
        
        for index in range(available_count):
            yield available_photos[index]