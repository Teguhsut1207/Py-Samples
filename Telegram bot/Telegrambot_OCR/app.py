import cv2
import numpy as np
from telegram import Update, File
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image
import pytesseract
import requests
from io import BytesIO
import os
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  #!for windows machine change to: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Set the TESSDATA_PREFIX environment variable
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/5/tessdata/"

# Preprocessing the image to enhance text visibility
def preprocess_image(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return Image.fromarray(binary)

# Define a function that will handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me a picture with text and I will extract it.')

# Define a function that will handle photo messages
async def photo_handler(update: Update, context: CallbackContext) -> None:
    try:
        # Get the photo file from the message
        photo_file: File = await update.message.photo[-1].get_file()
        photo_url = photo_file.file_path
        
        # Download the photo
        response = requests.get(photo_url)
        img = Image.open(BytesIO(response.content))
        
        # Preprocess the image
        processed_img = preprocess_image(img)
        
        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(processed_img, lang='eng')  #NOTE Specify language if needed
        
        # Respond with the extracted text
        await update.message.reply_text(f'Extracted text: {extracted_text}')
    except Exception as e:
        # Handle any errors that occur
        await update.message.reply_text(f"An error occurred: {e}")

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
