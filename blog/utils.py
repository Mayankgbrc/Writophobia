from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def get_image_url(post_obj, size = None):
    if size == 200:
        if post_obj.thumbnail_200:
            return post_obj.thumbnail_200
        elif post_obj.subcategory.thumbnail_200:
            return post_obj.subcategory.thumbnail_200
        return post_obj.category.thumbnail_200
    elif size == 500:
        if post_obj.thumbnail_500:
            return post_obj.thumbnail_500
        elif post_obj.subcategory.thumbnail_500:
            return post_obj.subcategory.thumbnail_500
        return post_obj.category.thumbnail_500
    if post_obj.thumbnail:
        return post_obj.thumbnail
    elif post_obj.subcategory.thumbnail:
        return post_obj.subcategory.thumbnail
    return post_obj.category.thumbnail

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

def clean_text_to_list(sentence):
    sentence_list = sentence.split()
    return [each for each in sentence_list if each not in stop_words]


def get_desired_height(im, desired_width):
    # get the width height ratio adjust
    original_width, original_height = im.size
    aspect_ratio = round(original_height / original_width,3)
    return int(desired_width * aspect_ratio)

def compress_image(self):
    # Opening the uploaded image
    im = Image.open(self.thumbnail).convert('RGB')
    img_name = self.thumbnail.name.split('.')[0]
    thumnail_width_list = [500, 200]
    for i in range(2):
        output = BytesIO()
        desired_width = thumnail_width_list[i]
        desired_height = get_desired_height(im, desired_width)
        img = im.resize((desired_width, desired_height))

        # after modifications, save it to the output
        img.save(output, format='JPEG', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        memory_upload = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % img_name, 'image/jpeg',
                                        sys.getsizeof(output), None)
        if i == 0: self.thumbnail_500 = memory_upload
        elif i == 1: self.thumbnail_200 = memory_upload
    return self

from django.utils.http import urlencode
import re

def encode_url(title, id):
    title = title.lower().replace(" ", "-")
    title = re.sub('[^\\w-]+','', title)
    return f"{title}-{id}"

def get_pk_from_url(pk):
    return pk.split("-")[-1]