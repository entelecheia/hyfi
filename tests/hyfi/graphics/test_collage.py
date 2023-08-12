from hyfi.main import HyFI
from pathlib import Path


def test_collage():
    url = "https://assets.entelecheia.ai/logo-square-512.png"
    url2 = "https://assets.entelecheia.ai/logo-circle-512.png"

    img = HyFI.load_image(url)
    img2 = HyFI.load_image(url2)

    cimg = HyFI.collage([img, img2], num_cols=2)
    assert cimg.image and cimg.image.size == (1054, 532)


def test_makegif():
    url = "https://assets.entelecheia.ai/logo-square-512.png"
    url2 = "https://assets.entelecheia.ai/logo-circle-512.png"

    HyFI.make_gif(
        [url, url2], output_file="workspace/test.gif", display_to_notebook=True
    )

    assert Path("workspace/test.gif").exists()


if __name__ == "__main__":
    test_collage()
    test_makegif()
