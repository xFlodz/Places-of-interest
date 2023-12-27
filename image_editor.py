def image_editor(image_list):
    new_image_list = []
    for i in image_list:
        new_image_list.append(i.path_to_image)
    return new_image_list