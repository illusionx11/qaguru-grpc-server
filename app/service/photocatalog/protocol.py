from typing import (
    Protocol,
    Iterator
)

from app.service.photocatalog.mock_repository import PhotoResponseModel

class Repository(Protocol):
    def get_photo(self, id_: str) -> PhotoResponseModel | None:
        ...
    
    def add_photo(self, photo: PhotoResponseModel) -> PhotoResponseModel:
        ...
    
    def get_random_photos(self, count: int) -> Iterator[PhotoResponseModel]:
        ...