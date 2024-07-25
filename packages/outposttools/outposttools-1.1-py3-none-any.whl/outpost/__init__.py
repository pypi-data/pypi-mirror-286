from .main import main
from .utils import get_image_path

__version__ = '1.0'
__all__ = ['main', 'get_image_path']

# Optionally perform some package initialization
def init():
    print("Initializing outpost package...")