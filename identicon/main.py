import argparse
import hashlib
from PIL import Image, ImageColor
import numpy as np

# An md5 hash is 32 characters. With this, we can create an 8x8, mirrored pattern.
# Split the md5 string into a 8 rows of 4 columns, flipping bits 'on' or 'off' 
# in the image depending on whether the unicode number of the character is even or odd.
# We can mirror this 8x4 image to achieve a nice symmetrical 8x8 image.
# To determine color, use the same white background for all, and generate the color from the hex code
# of the first 6 characters in the hash

BACKGROUND_COLOR = (255, 255, 255)
AVATAR_SIZE = 300
THUMBNAIL_SIZE = 100

parser = argparse.ArgumentParser(description="Generate a unique 5x5 identicon given a string input.")

parser.add_argument("input_string")
parser.add_argument("-o", "--output_file", default="img")
parser.add_argument("-s", "--size", default="400")

def hex_char_to_color(character, rgb_color):
    return rgb_color if ord(character) % 2 == 1 else BACKGROUND_COLOR

# Generates the 8x8 mirrored array with color values
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
    
    size = int(args.size)
    
    print(size)
    
    # Create and save image
    identicon = Image.fromarray(array)
    
    avatar = identicon.resize((AVATAR_SIZE, AVATAR_SIZE), Image.NONE)
    thumbnail = identicon.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.NONE)
    
    avatar.save("./{}-avatar.png".format(args.output_file))
    thumbnail.save("./{}-thumbnail.png".format(args.output_file))
    
main()