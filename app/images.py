import falcon
# import json
import msgpack


class Resource:
    # @staticmethod -> "TypeError: on_get() missing 1 required positional argument: 'resp'"
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
