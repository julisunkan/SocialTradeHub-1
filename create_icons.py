
from PIL import Image, ImageDraw
import os

# Create icons directory
os.makedirs('static/icons', exist_ok=True)

# Create a simple icon
def create_icon(size, filename):
    # Create a blue square with white text
    img = Image.new('RGB', (size, size), color='#3b82f6')
    draw = ImageDraw.Draw(img)
    
    # Add text (simplified)
    text = "SM"
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill='white')
    
    img.save(f'static/icons/{filename}')
    print(f'Created {filename}')

# Create required icons
create_icon(192, 'icon-192x192.png')
create_icon(512, 'icon-512x512.png')

print("Icons created successfully!")
