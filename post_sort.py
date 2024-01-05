def post_sort(posts, left_date, right_date):
    sorted_posts_list = []
    stack = []
    for post in posts:
        if post.left_date >= left_date:
            stack.append(post)
        else:
            pass
    for post in stack:
        if post.right_date <= right_date:
            sorted_posts_list.append(post)
        else:
            pass
    return sorted_posts_list



