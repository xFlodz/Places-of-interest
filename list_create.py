def create_images_list(count_images, list_of_images):
    new_list = []
    for i in range(max(count_images)+1):
        new_list.append('')
    n = 0
    for i in count_images:
        new_list[i] = list_of_images[n]
        n+=1
    return new_list


def create_videos_list(count_videos, list_of_videos):
    new_list = []
    for i in range(max(count_videos)+1):
        new_list.append('')
    n = 0
    for i in count_videos:
        new_list[i] = list_of_videos[n]
        n += 1
    return new_list

