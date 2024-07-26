import io
import logging

import cv2
import pytest
import pyvips
from PIL import Image
from turbojpeg import TurboJPEG

turbojpeg = TurboJPEG()
logger = logging.getLogger(name=None)


## encode frame to jpeg comparison


def pyvips_encode(frame_from_camera):
    # mute some other logger, by raising their debug level to INFO
    lgr = logging.getLogger(name="pyvips")
    lgr.setLevel(logging.WARNING)
    lgr.propagate = True
    # frame_from_camera = cv2.cvtColor(frame_from_camera, cv2.COLOR_BGR2RGB)
    out = pyvips.Image.new_from_array(frame_from_camera)
    bytes = out.write_to_buffer(".jpg[Q=85]")
    # im = Image.open(io.BytesIO(bytes))
    # im.show()

    return bytes


def turbojpeg_encode(frame_from_camera):
    # encoding BGR array to output.jpg with default settings.
    # 85=default quality
    bytes = turbojpeg.encode(frame_from_camera, quality=85)

    return bytes


def pillow_encode(frame_from_camera):
    image = Image.fromarray(frame_from_camera.astype("uint8"), "RGB")
    byte_io = io.BytesIO()
    image.save(byte_io, format="JPEG", quality=85)
    bytes_full = byte_io.getbuffer()

    return bytes_full


def cv2_encode(frame_from_camera):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encimg = cv2.imencode(".jpg", frame_from_camera, encode_param)

    return encimg


@pytest.fixture(params=["turbojpeg_encode", "pillow_encode", "cv2_encode", "pyvips_encode"])
def library(request):
    # yield fixture instead return to allow for cleanup:
    yield request.param

    # cleanup
    # os.remove(request.param)


def image(file):
    with open(file, "rb") as file:
        in_file_read = file.read()
        frame_from_camera = turbojpeg.decode(in_file_read)

    # yield fixture instead return to allow for cleanup:
    return frame_from_camera


@pytest.fixture()
def image_lores():
    yield image("tests/assets/input_lores.jpg")


@pytest.fixture()
def image_hires():
    yield image("tests/assets/input.jpg")


# needs pip install pytest-benchmark
@pytest.mark.benchmark(
    group="encode_lores",
)
def test_libraries_encode_lores(library, image_lores, benchmark):
    benchmark(eval(library), frame_from_camera=image_lores)
    assert True


# needs pip install pytest-benchmark
@pytest.mark.benchmark(
    group="encode_hires",
)
def test_libraries_encode_hires(library, image_hires, benchmark):
    benchmark(eval(library), frame_from_camera=image_hires)
    assert True
