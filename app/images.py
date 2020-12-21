import io
import os
import re
import uuid
import mimetypes

import falcon
# import json
import msgpack

ALLOWED_IMAGE_TYPES = (
    'image/git',
    'image/jpeg',
    'image/png',
)


def validate_image_type(req: falcon.Request, resp: falcon.Response, resource, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)


class ImageStore:
    _CHUNK_SIZE_BYTES = 4096
    _IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.[a-z]{2,4}$'
    )

    # Note the use of dependency injection for standard library methods.
    # We'll use these later to avoid monkey-patching.
    def __init__(self, storage_path: str, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, image_stream: falcon.Request.stream, image_content_type: str) -> str:
        ext = mimetypes.guess_extension(image_content_type)
        name = f'{self._uuidgen()}{ext}'
        image_path = os.path.join(self._storage_path, name)

        with self._fopen(image_path, 'wb') as image_file:
            while True:
                # By default Falcon does not spool or decode request data,
                # instead giving you direct access to the incoming binary stream provide by the WSGI server.
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        return name

    def open(self, name: str):
        # Always validate untrusted input!
        if not self._IMAGE_NAME_PATTERN.match(name):
            raise IOError('file not found')

        image_path = os.path.join(self._storage_path, name)
        stream = self._fopen(image_path, 'rb')
        content_length = os.path.getsize(image_path)

        return stream, content_length


class Collection:
    def __init__(self, image_store: ImageStore):
        self._image_store = image_store

    # If do '@staticmethod' -> "TypeError: on_get() missing 1 required positional argument: 'resp'"
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        # TODO: Modify this to return a list of href's based on
        # what images are actually available.
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_OK

    @falcon.before(validate_image_type)
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_CREATED
        resp.location = '/images/' + name


class Item:
    def __init__(self, image_store: ImageStore):
        self._image_store = image_store

    def on_get(self, req: falcon.Request, resp: falcon.Response, name: str):
        resp.content_type = mimetypes.guess_type(name)[0]
        resp.stream, resp.content_length = self._image_store.open(name)
