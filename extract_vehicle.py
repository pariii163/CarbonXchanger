import cv2
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_number_plate(image_path):
    """Detects vehicle number plate using EasyOCR"""
    img = cv2.imread(image_path)
    
    if img is None:
        print("❌ Error: Could not read the image. Check the file path!")
        return None

    # Convert to grayscale for better OCR detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR to detect text
    results = reader.readtext(gray)

    for (bbox, text, prob) in results:
        if len(text) >= 6:  # Filtering possible plate numbers
            return text.upper().replace(" ", "")

    return None

# Image path
image_path = r"C:\Users\shavy\OneDrive\Desktop\CodeSeva\NumberPlate\fancy_number_plate_bfbc501f34.jpg"

# Detect number plate
plate_number = detect_number_plate(image_path)

if plate_number:
    print(f"✅ Detected Vehicle Number: {plate_number}")
    print("Vehicle age is more than 15 years. Fine generated")
else:
    print("❌ Could not detect a valid number plate. Exiting.")


