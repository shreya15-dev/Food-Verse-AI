import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_media")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_image(filename, bg_color, title, subtitle):
    img = Image.new("RGB", (640, 480), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw simple food/kitchen geometry
    draw.rectangle([30, 30, 610, 450], outline=(255, 255, 255), width=3)
    draw.ellipse([200, 140, 440, 380], fill=(min(255, bg_color[0]+30), min(255, bg_color[1]+30), min(255, bg_color[2]+30)), outline=(255, 255, 255), width=2)
    
    # Text
    draw.text((320, 70), title, fill=(255, 255, 255), anchor="mm")
    draw.text((320, 110), subtitle, fill=(240, 240, 240), anchor="mm")
    
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path, quality=92)
    print(f"Created: {path}")

# Generate sample food images
create_image("food_quinoa_salad.jpg", (38, 92, 60), "Mediterranean Quinoa Bowl", "Fresh Greens, Olives, Chickpeas, Olive Oil")
create_image("food_grilled_chicken.jpg", (160, 90, 44), "Herb Grilled Chicken Breast", "Lean Protein with Steamed Broccoli")
create_image("food_margherita_pizza.jpg", (190, 45, 30), "Neapolitan Margherita Pizza", "San Marzano Tomatoes, Basil & Mozzarella")

# Generate sample produce images
create_image("fresh_crisp_apple.jpg", (185, 28, 28), "Crisp Ripe Red Apple", "Smooth skin, intact stem, optimal turgor")
create_image("produce_browning_decay.jpg", (110, 65, 25), "Produce Deterioration Sample", "Oxidation spots, surface softening, aging")

# Generate kitchen photos
create_image("kitchen_prep_clean.jpg", (30, 58, 95), "Commercial Prep Kitchen Station", "Sanitized stainless steel counters, clean cutting boards")
create_image("kitchen_prep_cluttered.jpg", (80, 40, 40), "Kitchen Station with Observations", "Uncovered ingredients, station clutter, waste proximity")

# Generate a real valid MP4 video using OpenCV
video_path = os.path.join(OUTPUT_DIR, "kitchen_audit_walkthrough.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 10.0
width, height = 480, 360
out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

# Create 40 frames (4 seconds) of a simulated kitchen walkthrough panning across prep stations
for i in range(40):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    # Background stainless steel tone with subtle shifting gradient
    base_val = int(80 + 30 * np.sin(i / 10.0))
    frame[:] = (base_val + 20, base_val + 10, base_val)
    
    # Draw simulated stainless counter line
    cv2.line(frame, (0, 240), (width, 240), (200, 200, 200), 3)
    
    # Draw moving inspection marker / cutting board
    box_x = int(60 + (i * 7) % 300)
    cv2.rectangle(frame, (box_x, 160), (box_x + 90, 240), (50, 140, 70), -1)
    cv2.rectangle(frame, (box_x + 120, 180), (box_x + 170, 240), (40, 70, 160), -1)
    
    # Timestamp overlay
    sec = i / fps
    cv2.putText(frame, f"Kitchen CCTV Cam 02 - Time: 00:{sec:04.1f}s", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.putText(frame, "Food Verse AI Video Inspection Test Clip", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 240, 200), 1)
    
    out.write(frame)

out.release()
print(f"Created real MP4 video: {video_path}")
