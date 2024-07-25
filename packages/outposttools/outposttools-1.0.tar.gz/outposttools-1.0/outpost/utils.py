import pkg_resources

def get_image_path(filename):
    return pkg_resources.resource_filename(__name__, f'images/{filename}')
