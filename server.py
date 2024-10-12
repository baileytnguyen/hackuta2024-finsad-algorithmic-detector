from concurrent import futures
import grpc
import comment_scam_detector_pb2
import comment_scam_detector_pb2_grpc
import re
from nameparser import HumanName  # Importing the nameparser library

# Define the full name pattern for initial detection
full_name_pattern = re.compile(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+)+|[A-Z]+\s[A-Z]+\s[A-Z]+)\b")

# Function to detect scams in comments
def detect_scam_in_comments(comments):
    # Define keywords to identify scam comments
    scam_keywords = [
        "licensed", "advisor", "contact", "look up", "research",
        "one-off", "benefit", "returns", "charge", "genius",
        "experience", "essential", "name", "appointment"
    ]

    suspicion_score = 0  # Initialize suspicion score

    # Check for keywords and names in comments
    for comment in comments:
        comment_text = comment.comment_text
        print(f"Analyzing comment: {comment_text}")  # Debug output
        
        # Check for keywords
        if any(keyword in comment_text.lower() for keyword in scam_keywords):
            print("Scam keyword detected.")  # Debug output
            suspicion_score += 1  # Increment score for keyword presence
        
        # Check for full names using nameparser
        name = HumanName(comment_text)  # Parse the comment text as a name
        if name.first and name.last:  # Check if a first and last name were detected
            print("Full name detected using nameparser.")  # Debug output
            suspicion_score += 5  # Boost score for name presence

        # Check for all uppercase words
        if any(word.isupper() for word in comment_text.split()):
            print("All caps detected.")  # Debug output
            suspicion_score += 3  # Boost score for all caps

    # Determine if a scam is detected based on suspicion score
    is_scam = suspicion_score > 5  # Set threshold for scam detection
    confidence = suspicion_score / 10  # Confidence score as a fraction of maximum score

    return is_scam, confidence  # Return scam detection result and confidence score

# Create the service class
class ScamDetectionServiceServicer(comment_scam_detector_pb2_grpc.ScamDetectionServiceServicer):
    def DetectScam(self, request, context):
        thread = request.thread.comments
        scam_found, confidence = detect_scam_in_comments(thread)

        # Create the response
        response = comment_scam_detector_pb2.ScamDetectionResponse(
            is_scam=scam_found,
            message="Scam detected" if scam_found else "No scam detected",
            confidence=confidence
        )
        return response

# Function to start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comment_scam_detector_pb2_grpc.add_ScamDetectionServiceServicer_to_server(ScamDetectionServiceServicer(), server)
    server.add_insecure_port('[::]:50051')  # The port the server will listen on
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
