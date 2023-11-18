import os
def delete_images(post):
    if post.post_images:
        post_images = post.post_images
        post_images = post_images.split(' ')
        post_images.pop()
        for i in post_images:
            os.remove(i)

def delete_main(post):
    os.remove(post.main_image)
