import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def extract_text_from_image (image_url):
    

    # Define prompt based on client instructions
    prompt = """
   Extract the energy efficiency values from the given EPC rating chart.

The chart contains three key values:
1. **Current Score** (a numerical value Current Score )
2. **Potential Score** (another numerical value Potential Score)
3. **Rating** (A-G scale based on the Current Score mapping)

### **Rating Scale:**
- A: 92+
- B: 81-91
- C: 69-80
- D: 55-68
- E: 39-54
- F: 21-38
- G: 1-20

Return the extracted values in **pure JSON format**, with **no additional text, markdown, or formatting**:

{
    "current_score": VALUE,
    "potential_score": VALUE,
    "rating": "LETTER"
}

    """
    
    # Send request to OpenAI API with properly formatted image input
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract the EPC values from this image."},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ]
    )
    
    # Extract and print the response
    output_text = response["choices"][0]["message"]["content"]
    return output_text
    