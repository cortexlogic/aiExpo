import urllib.request
import time
import datetime
import glob

camera_codes = ['201B', '201C', '201D', '203', '203A', '204', '205', '206',
                '206A', '208', '209', '211', '212', '213', '214', '215', '216',
                '217']

while(True):
    for code in camera_codes:
        ts = str(datetime.datetime.now().timestamp()).split('.')[0]
        urllib.request.urlretrieve(
            f'https://www.i-traffic.co.za/map/Cctv/WC%20CCTV%20N2%20{code}--4',
            f'images/camera_{code}_{ts}.jpg'
        )
    n_img = len(glob.glob('images/*.jpg'))
    print(f'number of images in `images`: {n_img}')
    time.sleep(60)
