import requests
from bs4 import BeautifulSoup
from PIL import Image
import os
from io import BytesIO
import csv
from datetime import datetime
import wordpress_xmlrpc
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import media

class BlogImageMigrator:
    def __init__(self, blogspot_url, wp_url, wp_username, wp_password):
        self.blogspot_url = blogspot_url
        self.wp_client = Client(
            f'{wp_url}/xmlrpc.php',
            wp_username,
            wp_password
        )
        self.temp_dir = 'temp_images'
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def extract_image_urls(self):
        """Extract image URLs from Blogspot"""
        response = requests.get(self.blogspot_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        
        image_urls = []
        for img in images:
            if img.get('src'):
                url = img['src']
                if url.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_urls.append(url)
        
        return image_urls
    
    def convert_to_webp(self, image_data, quality=65):
        """Convert image to WebP format with compression"""
        img = Image.open(BytesIO(image_data))
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        
        # Prepare output buffer
        output = BytesIO()
        
        # Convert and compress to WebP
        img.save(output, format='WEBP', quality=quality)
        output.seek(0)
        
        return output
    
    def upload_to_wordpress(self, image_data, filename):
        """Upload image to WordPress"""
        data = {
            'name': f'{filename}.webp',
            'type': 'image/webp',
            'bits': wordpress_xmlrpc.BytesIO(image_data.read()),
        }
        
        try:
            response = self.wp_client.call(media.UploadFile(data))
            return response
        except Exception as e:
            print(f"Error uploading {filename}: {str(e)}")
            return None
    
    def process_images(self):
        """Main process to handle the image migration"""
        # Get image URLs
        print("Extracting image URLs from Blogspot...")
        image_urls = self.extract_image_urls()
        
        # Prepare CSV for logging
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'migration_log_{timestamp}.csv'
        
        with open(log_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Original URL', 'WordPress URL', 'Status'])
            
            for i, url in enumerate(image_urls, 1):
                print(f"Processing image {i}/{len(image_urls)}: {url}")
                
                try:
                    # Download image
                    response = requests.get(url)
                    if response.status_code != 200:
                        writer.writerow([url, '', 'Download Failed'])
                        continue
                    
                    # Convert to WebP
                    webp_data = self.convert_to_webp(response.content)
                    
                    # Generate filename from original URL
                    filename = os.path.splitext(url.split('/')[-1])[0]
                    
                    # Upload to WordPress
                    upload_response = self.upload_to_wordpress(webp_data, filename)
                    
                    if upload_response:
                        writer.writerow([url, upload_response['url'], 'Success'])
                        print(f"Successfully uploaded: {filename}")
                    else:
                        writer.writerow([url, '', 'Upload Failed'])
                
                except Exception as e:
                    writer.writerow([url, '', f'Error: {str(e)}'])
                    print(f"Error processing {url}: {str(e)}")
        
        print(f"\nMigration complete. Log file saved as: {log_file}")

# Example usage
if __name__ == "__main__":
    # Configuration
    BLOGSPOT_URL = "https://your-blog.blogspot.com"
    WP_URL = "https://your-wordpress-site.com"
    WP_USERNAME = "your_username"
    WP_PASSWORD = "your_password"
    
    # Initialize and run migration
    migrator = BlogImageMigrator(BLOGSPOT_URL, WP_URL, WP_USERNAME, WP_PASSWORD)
    migrator.process_images()
