import io
import os
import uuid
import mimetypes

import falcon
# import json
import msgpack


class ImageStore:

    _CHUNK_SIZE_BYTES = 4096

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


class Resource:

    # The resource object must now be initialized with a path used during POST
    def __init__(self, image_store: ImageStore):
        self._image_store = image_store

    # If do '@staticmethod' -> "TypeError: on_get() missing 1 required positional argument: 'resp'"
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        # Create a JSON representation of the resource
        # resp.body = json.dumps(doc, ensure_ascii=False)

        # Using msgpack-python
        # a small performance gain by assigning directly to resp.data
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_OK

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_CREATED
        resp.location = '/images/' + name
