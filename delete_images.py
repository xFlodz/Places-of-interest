import os
def delete_images(post):
    os.remove(post.main_image)
    if post.post_images:
        post_images = post.post_images
        post_images = post_images.split(' ')
        post_images.pop()
        for i in post_images:
            os.remove(i)