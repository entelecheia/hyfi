from hyfi.main import HyFI
from hyfi.graphics.utils import get_default_system_font


def test_load_image():
    url = "https://assets.entelecheia.ai/logo-square-512.png"

    img = HyFI.load_image(url)
    assert img.size == (512, 512)

    img = HyFI.scale_image(img, max_width=256)
    assert img.size == (256, 256)


def test_get_image_font():
    print(get_default_system_font(lang="en"))
    font = HyFI.get_image_font()
    print(font)
    assert font and font.size == 12


if __name__ == "__main__":
    test_load_image()
    test_get_image_font()
