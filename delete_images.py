import os
def delete_images(iitp):
    for image in iitp:
        path_to_image = image.path_to_image
        os.remove(path_to_image)

def delete_main(post):
    os.remove(post.main_image)
