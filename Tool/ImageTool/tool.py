import os

def get_imlist(path,suffix='.png'):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith(suffix)]
