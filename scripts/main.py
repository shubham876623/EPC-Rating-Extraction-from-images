from database.db_connector import fetch_image_urls, update_database
from extractor.image_processor import extract_text_from_image
import json

def process_images():
    """Processes images, extracts text data, and updates the database only if rating is missing or invalid."""
    images = fetch_image_urls()
    
    for image in images:
        property_id = int(image[0])
        existing_rating = image[2]  
        print(image[1])
        if image[1] is not None and "None" not in image[1]:
            # Skip processing if rating is already present and valid
            if existing_rating and existing_rating not in ["0", 0, None, "Not Available"]:
                print(f"Skipping property ID {property_id} (Rating: {existing_rating})")
                continue
            # print(f"Processing property ID {property_id} (Existing Rating: {existing_rating})")
            image_url = image[1]
            try:
                text_output = extract_text_from_image(image_url)
                data = json.loads(text_output)
    
                update_data = [
                    property_id,
                    data.get("rating"),
                    data.get("current_score"),
                    data.get("potential_score")
                ]
    
                update_database(update_data)
            except:
                update_data = [property_id, 0, 0, 0]
                update_database(update_data)
        else:
            # print(f"Image url is None for the {property_id}")
            update_data = [property_id, 0, 0, 0]
            update_database(update_data)

if __name__ == "__main__":
    process_images()
