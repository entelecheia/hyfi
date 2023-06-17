from hyfi.main import HyFI


def test_collage():
    url = "https://assets.entelecheia.ai/logo-square-512.png"
    url2 = "https://assets.entelecheia.ai/logo-circle-512.png"

    img = HyFI.load_image(url)
    img2 = HyFI.load_image(url2)

    cimg = HyFI.collage([img, img2], cols=2)
    assert cimg.image and cimg.image.size == (1054, 532)


if __name__ == "__main__":
    test_collage()
