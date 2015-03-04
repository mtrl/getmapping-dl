import time
import urllib2
import webbrowser
import os
from PIL import Image

images_dir = "getmapping"
# start and end coordinates
# x from left to right incrementing
start_x = 343544
end_x = 344244
# x from top to bottom decrement
start_y = 327094
end_y = 326294


x_inc = 100
y_inc = 53

# pause so we don't break stuff
wait = 0.5

url = "https://www2.getmapping.com/Webshop/web/CommonPages/Main/IEDPreview.aspx?Dataset=2012_UK_125mm&ResolutionInMetres=0.1&CentreX=[[X]]&CentreY=[[Y]]"

cols = 0
rows = 0

the_counter = 1

def download_images():
    global the_counter
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    user_agent = 'Mozilla/5 (Solaris 10) Gecko'
    headers = { 'User-Agent' : user_agent }
    cur_y = start_y
    while cur_y > end_y:
        global cols
        cols = 0
        
        cur_x = start_x
        while cur_x < end_x:
            #print str(cur_x) + " " + str(cur_y)
            image_url = url.replace('[[X]]',str(cur_x))
            image_url = image_url.replace('[[Y]]',str(cur_y))
            print image_url
            # wait so we dont kill it
            time.sleep(wait)
            #image_file = urllib.URLopener(headers=headers)
            request = urllib2.Request(image_url, headers=headers)
            image_data = urllib2.urlopen(request).read()
            output = open(images_dir + "//" + str(the_counter) + ".jpeg",'wb')
            output.write(image_data)
            output.close()
            
            the_counter += 1
            cur_x += x_inc
            cols += 1
        cur_y -= y_inc
        
        global rows
        rows += 1
    print rows
    print cols
    
def stitch_images():
    # size and grid values
    img_w = 1000
    img_h = 530
    global cols
    global rows
    buf = 0 # space between image tiles
    
    # this assumes images are all of size 1800x1800
    size = ((img_w * cols) + (buf * cols) + buf, (img_h * rows) + (buf * rows) + buf)
    
    
    # create new image to paste files into
    im2 = Image.new("RGB", size, "#eee")
    
    # initialize which column and row to start
    col = 0
    row = 0
    
    # paste images into one big image
    global the_counter
    for i in range(1,the_counter):
        # should make system independent separator
        im = Image.open(images_dir + "//" + str(i) + ".jpeg") 
    
        box = ((im.size[0]*col) + (buf * col) + buf,
            (im.size[1]*row) + (buf*row) + buf)
    
        im2.paste(im, box)
    
        # get ready for next image
        if col < (cols-1): 
            col += 1
        else:
            col = 0
            row += 1
    
    
    # now that we're done, save the results
    im2.save(images_dir + "//" + images_dir + ".jpg")
    print "Created stitched image"
    
if __name__ == "__main__":
    download_images()
    stitch_images()