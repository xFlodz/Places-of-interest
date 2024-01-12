def image_editor(image_list):
    for i in range(len(image_list)):
        if image_list[i] != '':
            image_list[i] = image_list[i].path_to_image
    return image_list