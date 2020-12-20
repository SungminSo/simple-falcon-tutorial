import io
import os
import uuid
import mimetypes

import falcon
# import json
import msgpack


class Resource:
    _CHUNK_SIZE_BYTES = 4096

    # The resource object must now be initialized with a path used during POST
    def __init__(self, storage_path):
        self._storage_path = storage_path

    # If do '@staticmethod' -> "TypeError: on_get() missing 1 required positional argument: 'resp'"
    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        # Create a JSON representation of the resource
        # resp.body = json.dumps(doc, ensure_ascii=False)

        # using msgpack-python
        # a small performance gain by assigning directly to resp.data
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp):
        ext = mimetypes.guess_extension(req.content_type)
        name = f'{uuid.uuid4()}{ext}'
        image_path = os.path.join(self._storage_path, name)

        print(image_path)

        with io.open(image_path, 'wb') as image_file:
            while True:
                # By default Falcon does not spool or decode request data,
                # instead giving you direct access to the incoming binary stream provide by the WSGI server.
                chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        resp.status = falcon.HTTP_CREATED
        resp.location = '/storage/' + name
