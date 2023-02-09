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