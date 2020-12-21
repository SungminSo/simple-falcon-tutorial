import os
import falcon

from .images import ImageStore, Collection, Item


def create_app(image_store: ImageStore) -> falcon.API:
    api = falcon.API()

    api.add_route('/images', Collection(image_store=image_store))
    api.add_route('/images/{name}', Item(image_store=image_store))
    return api


def get_app() -> falcon.API:
    storage_path = os.environ.get('APP_STORAGE_PATH', 'storage')
    image_store = ImageStore(storage_path=storage_path)
    return create_app(image_store=image_store)
