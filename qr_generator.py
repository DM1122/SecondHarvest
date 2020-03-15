import qrcode
import PIL
from PIL import Image
import random
import os
import shutil



def genIDs(count=5):
    '''
    Returns a list of unique identification codes.
    '''

    ids = random.sample(range(10000000,99999999), k=count)     # samples from very large distribution. Does not allow collisions.


    return ids


def pasteLogo(img, logo_path, scl=1):
    '''
    Overlays qr img with logo.
    '''
    # open and scale logo
    logo = PIL.Image.open(logo_path)
    new_size = (int(logo.size[0]*scl), int(logo.size[1]*scl))
    logo = logo.resize(new_size) 


    # put the logo in the qr code
    pos = ((img.size[0]//2)-logo.size[0]//2, (img.size[1]//2)-logo.size[1]//2)      # position at center of img
    img.paste(logo, pos, logo)



if __name__ == '__main__':
    shutil.rmtree('output') if os.path.exists('output') else False          # will clear output directory after each run
    os.makedirs('output') if not os.path.exists('output') else False

    # generate id codes
    ids = genIDs(count=10)

    # iterate through each id
    for idd in ids:
        qr = qrcode.QRCode(
            version=1,                                              # 21x21 matrix
            error_correction=qrcode.constants.ERROR_CORRECT_M,      # %15 error correction to enable logo placement
            box_size=32,
            border=4,
        )
        qr.add_data(idd)
        qr.make()

        img = qr.make_image(fill_color='black', back_color='white')
        img = img.convert('RGBA')

        pasteLogo(img, 'assets/logo_trans_fill.png', scl=0.3)
        
        img.save('output/'+str(idd)+'.png')