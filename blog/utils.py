
def get_image_url(post_obj):
    if post_obj.thumbnail:
        return post_obj.thumbnail
    elif post_obj.subcategory.thumbnail:
        return post_obj.subcategory.thumbnail
    return post_obj.category.thumbnail