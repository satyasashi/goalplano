from django.conf import settings


def get_user_directory_thumbnail_path(username, img_name):
    img_name = img_name.name.split("/")[-1]
    return settings.MEDIA_ROOT + f"/{username}/profile_pics/{img_name}"
