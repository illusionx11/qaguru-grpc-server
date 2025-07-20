import internal.pb.photocatalog_pb2_grpc as photocatalog_pb2_grpc
import internal.pb.photocatalog_pb2 as photocatalog_pb2
from grpc import ServicerContext, StatusCode
from typing import Iterator
import google.protobuf.timestamp_pb2 as timestamp_pb2
from app.service.photocatalog.protocol import Repository
from app.service.photocatalog.mock_repository import PhotoResponseModel, TimestampModel
from datetime import datetime
import uuid

class PhotoCatalogService(photocatalog_pb2_grpc.PhotoCatalogServiceServicer):
    
    def __init__(self, repository: Repository):
        self._repository = repository
        
    def Photo(
        self, request: photocatalog_pb2.IdRequest, context: ServicerContext
    ) -> photocatalog_pb2.PhotoResponse:
        photo = self._repository.get_photo(request.id)
        if not photo:
            context.abort(StatusCode.NOT_FOUND, f"Photo with id {request.id} not found")
            return photocatalog_pb2.PhotoResponse()
        
        response = photocatalog_pb2.PhotoResponse(
            id=photo.id,
            description=photo.description,
            timestamp=timestamp_pb2.Timestamp(
                seconds=photo.timestamp.seconds,
                nanos=photo.timestamp.nanos
            ),
            content=photo.content
        )
        return response
    
    def AddPhoto(
        self, request: photocatalog_pb2.PhotoRequest, context: ServicerContext
    ) -> photocatalog_pb2.PhotoResponse:
        id_ = str(uuid.uuid4())
        photo_response = self._repository.add_photo(
            photo=photocatalog_pb2.PhotoResponse(
                id=id_,
                description=request.description,
                content=request.content
            )
        )
        now = timestamp_pb2.Timestamp()
        now.FromDatetime(datetime.now())
        photo_response.timestamp.CopyFrom(now)
        
        photo_model = PhotoResponseModel(
            id=photo_response.id,
            description=photo_response.description,
            timestamp=TimestampModel(
                seconds=photo_response.timestamp.seconds,
                nanos=photo_response.timestamp.nanos
            ),
            content=photo_response.content
        )
        self._repository.add_photo(photo_model)
        
        return photo_response
    
    def RandomPhotos(
        self, request: photocatalog_pb2.CountRequest, context: ServicerContext
    ) -> Iterator[photocatalog_pb2.PhotoResponse]:
        for photo in self._repository.get_random_photos(request.count):
            response = photocatalog_pb2.PhotoResponse(
                id=photo.id,
                description=photo.description,
                timestamp=timestamp_pb2.Timestamp(
                    seconds=photo.timestamp.seconds,
                    nanos=photo.timestamp.nanos
                ),
                content=photo.content
            )
            yield response
    
    def UploadPhotos(
        self, request_iterator: Iterator[photocatalog_pb2.PhotoUploadRequest], context: ServicerContext
    ) -> photocatalog_pb2.UploadResponse:
        uploaded_count = 0
        now = timestamp_pb2.Timestamp()
        now.FromDatetime(datetime.now())
        
        try:
            for request in request_iterator:
                photo_id = str(uuid.uuid4())
                
                photo_model = PhotoResponseModel(
                    id=photo_id,
                    description=request.description,
                    timestamp=TimestampModel(
                        seconds=now.seconds,
                        nanos=now.nanos
                    ),
                    content=request.content
                )
                
                self._repository.add_photo(photo_model)
                uploaded_count += 1
            
            return photocatalog_pb2.UploadResponse(
                success=True,
                message=f"Количество загруженных фотографий: {uploaded_count}",
                uploaded_count=uploaded_count
            )
            
        except Exception as e:
            return photocatalog_pb2.UploadResponse(
                success=False,
                message=f"Ошибка при загрузке фотографий: {str(e)}",
                uploaded_count=uploaded_count
            )