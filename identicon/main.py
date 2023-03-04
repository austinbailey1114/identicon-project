import argparse
import hashlib
from PIL import Image, ImageColor
import numpy as np

BACKGROUND_COLOR = (255, 255, 255)
AVATAR_SIZE = 300
THUMBNAIL_SIZE = 100

parser = argparse.ArgumentParser(description="Generate a unique 8x8 identicon given a string input.")
parser.add_argument("input_string")
parser.add_argument("-o", "--output_file_name", default="img")

def hex_char_to_color(character, rgb_color):
    return rgb_color if ord(character) % 2 == 1 else BACKGROUND_COLOR

# Generates the 8x8 mirrored array with color values. This iterates through every 4 items
# in the hash and adds its own reversed value to itself, creating the mirroring effect. 
def generate_pixel_array(hash, rgb_color):
    return [[hex_char_to_color(x, rgb_color) for x in hash[i:i+4] + hash[i:i+4][::-1]] for i in range (0, len(hash), 4)]       

def main():
    # Automatically handles badly formatted args, and shows help with -h argument
    args = parser.parse_args()
        
    # Get the hash as a string
    hash = hashlib.md5(args.input_string.encode()).hexdigest()
    
    # Convert first 6 hexadecimal characters of hash to RGB color
    rgb_color = ImageColor.getrgb('#{}'.format(hash[:6]))
    
    pixels = generate_pixel_array(hash, rgb_color)
        
    # Convert to a numpy array, as thats that the PIL library uses
    array = np.array(pixels, dtype=np.uint8)

    identicon = Image.fromarray(array)
    
    # Upscale to avatar and thumbnail sizes
    avatar = identicon.resize((AVATAR_SIZE, AVATAR_SIZE), Image.NONE)
    thumbnail = identicon.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.NONE)
    
    avatar.save("./{}-avatar.png".format(args.output_file_name))
    thumbnail.save("./{}-thumbnail.png".format(args.output_file_name))
    
    print("Successfully saved images for input {}".format(args.input_string))
    
main()