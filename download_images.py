import os
import requests
from urllib.parse import urlparse

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded: {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# Create images directory if it doesn't exist
IMAGES_DIR = 'static/images'
os.makedirs(IMAGES_DIR, exist_ok=True)

# Dictionary of images to download
images = {
    # Hero section background
    'hero-bg.jpg': 'https://images.unsplash.com/photo-1539635278303-d4002c07eae3?q=80&w=2070&auto=format&fit=crop',
    
    # Newsletter section background
    'newsletter-bg.jpg': 'https://images.unsplash.com/photo-1565609537938-14d88e26cdf5?q=80&w=2070&auto=format&fit=crop',
    
    # Popular destinations
    'marrakech.jpg': 'https://images.pexels.com/photos/3889843/pexels-photo-3889843.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'fes.jpg': 'https://images.pexels.com/photos/3889854/pexels-photo-3889854.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'chefchaouen.jpg': 'https://images.pexels.com/photos/4388164/pexels-photo-4388164.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'sahara.jpg': 'https://images.pexels.com/photos/4553618/pexels-photo-4553618.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    
    # Umrah services
    'umrah-hero.jpg': 'https://images.pexels.com/photos/2526935/pexels-photo-2526935.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'mecca.jpg': 'https://images.pexels.com/photos/5550501/pexels-photo-5550501.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'medina.jpg': 'https://images.pexels.com/photos/4039921/pexels-photo-4039921.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    
    # Blog placeholder
    'blog-placeholder.jpg': 'https://images.unsplash.com/photo-1526495124232-a04e1849168c?q=80&w=1000&auto=format&fit=crop',
    
    # Logo and favicon
    'logo.png': 'https://img.freepik.com/free-vector/detailed-travel-logo_23-2148616611.jpg?w=740&t=st=1701307254~exp=1701307854~hmac=60d08d531d07d5052bfb16feaf54d8ee6a4bb8c9c3c0f6d0f0f9f33f8b4c0b9',
    'favicon.ico': 'https://img.freepik.com/free-vector/detailed-travel-logo_23-2148616611.jpg?w=32&t=st=1701307254~exp=1701307854~hmac=60d08d531d07d5052bfb16feaf54d8ee6a4bb8c9c3c0f6d0f0f9f33f8b4c0b9'
}

# Download each image
for filename, url in images.items():
    save_path = os.path.join(IMAGES_DIR, filename)
    download_image(url, save_path)
