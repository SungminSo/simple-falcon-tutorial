import falcon

from .images import Resource, ImageStore


def create_app(image_store: str) -> falcon.API:
    api = falcon.API()

    api.add_route('/images', Resource(image_store=image_store))

    return api


def get_app() -> falcon.API:
    image_store = ImageStore(storage_path='storage')
    return create_app(image_store=image_store)
