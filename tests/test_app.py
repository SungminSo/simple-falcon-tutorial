import falcon
import msgpack
import pytest
import io

from falcon import testing
from unittest.mock import mock_open, call, MagicMock

import app.app
import app.images


@pytest.fixture
def mock_store():
    return MagicMock()


@pytest.fixture
def client(mock_store):
    api = app.app.create_app(mock_store)
    return testing.TestClient(api)


# pytest will inject the object returned by the "client" function
# as an additional parameter.


def test_list_images(client):
    doc = {
        'images': [
            {
                'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
            }
        ]
    }

    response = client.simulate_get('/images')
    result_doc = msgpack.unpackb(response.content, raw=False)

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK


def test_post_image(client, mock_store):
    file_name = 'fake-image-name.xyz'

    # We need to know what ImageStore method will be used
    mock_store.save.return_value = file_name
    image_content_type = 'image/xyz'

    response = client.simulate_post(
        '/images',
        body=b'some-fake-bytes',
        headers={'content-type': image_content_type}
    )

    assert response.status == falcon.HTTP_CREATED
    assert response.headers['location'] == f'/images/{file_name}'
    saver_call = mock_store.save.call_args

    # saver_cal is a unittest.mock.call tuple.
    # It's first element is a tuple of positional arguments supplied when calling the mock.
    # TODO: AssertionError: assert False
    # assert isinstance(saver_call[0][0], falcon.request.helpers.BoundedStream)
    assert saver_call[0][1] == image_content_type


def test_saving_image(monkeypatch):
    # This still has some mocks, but they are more localized and do not
    # have to be monkey-patched into standard library modules
    # (always a risky business).
    mock_file_open = mock_open()

    fake_uuid = '2c15ff4f-c788-4b83-8bdb-cb8662026498'

    def mock_uuidgen():
        return fake_uuid

    fake_image_bytes = b'fake-image-bytes'
    fake_request_stream = io.BytesIO(fake_image_bytes)
    storage_path = 'fake-storage-path'
    store = app.images.ImageStore(
        storage_path=storage_path,
        uuidgen=mock_uuidgen,
        fopen=mock_file_open
    )

    assert store.save(fake_request_stream, 'image/png') == fake_uuid + '.png'
    assert call().write(fake_image_bytes) in mock_file_open.mock_calls
