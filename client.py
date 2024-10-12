import grpc
import comment_scam_detector_pb2
import comment_scam_detector_pb2_grpc

def run():
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')
    
    # Create a stub (client)
    stub = comment_scam_detector_pb2_grpc.ScamDetectionServiceStub(channel)
    
    # Create a comment thread with the specified comment
    comments = [
        comment_scam_detector_pb2.Comment(
            user_id="1", 
            username="user1", 
            comment_text="licensed", 
            timestamp=1632876000  # Example timestamp
        )
    ]
    
    # Create a thread with the comments
    thread = comment_scam_detector_pb2.CommentThread(comments=comments)
    
    # Create a request
    request = comment_scam_detector_pb2.ScamDetectionRequest(thread=thread)
    
    # Call the DetectScam method
    response = stub.DetectScam(request)
    
    # Print the response
    print(f"Scam detected: {response.is_scam}")
    print(f"Message: {response.message}")
    print(f"Confidence: {response.confidence}")

if __name__ == '__main__':
    run()
