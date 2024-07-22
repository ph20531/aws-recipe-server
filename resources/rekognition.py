from flask import request
from flask_restful import Resource
from PIL import Image, ImageDraw
from config import Config
import boto3
import os

rekognition = boto3.client('rekognition', region_name=Config.REGION_NAME,
                           aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

reference_image_path = r'uploads\face_1.jpg'
with open(reference_image_path, 'rb') as f:
    reference_image_bytes = f.read()

class Rekognition1(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file part in the request"}, 400
        
        uploaded_file = request.files['file']
        
        # Read uploaded image
        uploaded_image = uploaded_file.read()

        # Call AWS Rekognition to compare faces
        response = rekognition.compare_faces(
            SourceImage={'Bytes': reference_image_bytes},
            TargetImage={'Bytes': uploaded_image},
            SimilarityThreshold=80  # Adjust as needed (0-100)
        )

        # Process AWS Rekognition response
        if len(response['FaceMatches']) > 0:
            similarity_score = response['FaceMatches'][0]['Similarity']
            return {"similarity_score": similarity_score}, 200
        else:
            return {"message": "No matching faces found"}, 404
        


class Rekognition2(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file part in the request"}, 400
        
        # Read uploaded image
        uploaded_file = request.files['file']
        uploaded_image = uploaded_file.read()

        # Call AWS Rekognition to compare faces
        response = rekognition.compare_faces(
            SourceImage={'Bytes': reference_image_bytes},
            TargetImage={'Bytes': uploaded_image},
            SimilarityThreshold=80  # Adjust as needed (0-100)
        )

        # Process AWS Rekognition response
        if len(response['FaceMatches']) > 0:
            # Load uploaded image using PIL
            img = Image.open(uploaded_file)
            draw = ImageDraw.Draw(img)

            # Iterate over each matching face
            for match in response['FaceMatches']:
                face = match['Face']
                # Get bounding box information
                bbox = face['BoundingBox']
                width, height = img.size
                left = bbox['Left'] * width
                top = bbox['Top'] * height
                right = left + (bbox['Width'] * width)
                bottom = top + (bbox['Height'] * height)

                # Draw red rectangle around the face
                draw.rectangle([left, top, right, bottom], outline='red', width=3)

            # Save the modified image in the upload folder
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            save_path = os.path.join(UPLOAD_FOLDER, 'highlighted_faces.jpg')
            img.save(save_path)

            return {"message": "Successfully highlighted matching faces", "image_path": save_path}, 200
        else:
            return {"message": "No matching faces found"}, 404