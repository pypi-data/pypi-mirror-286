import pkg_resources

def get_image_path(filename):
    print(f'Getting image path for {pkg_resources.resource_filename(__name__, f"images/{filename}")}')
    return pkg_resources.resource_filename(__name__, f'images/{filename}')
