import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grpc
from grpc_reflection.v1alpha import reflection
import time
from concurrent import futures
import internal.pb.photocatalog_pb2_grpc as photocatalog_pb2_grpc
import internal.pb.photocatalog_pb2 as photocatalog_pb2
from app.service.photocatalog.service import PhotoCatalogService
from app.service.photocatalog.mock_repository import MockRepository

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    repository = MockRepository()
    service = PhotoCatalogService(repository)
    
    photocatalog_pb2_grpc.add_PhotoCatalogServiceServicer_to_server(
        service, server
    )
    
    SERVICE_NAMES = (
        photocatalog_pb2.DESCRIPTOR.services_by_name['PhotoCatalogService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    
    print("Server started")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")
        
if __name__ == "__main__":
    serve()