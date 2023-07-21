from hyfi.main import HyFI


def test_save_wordlist():
    words = ["hello", "world", "Hello", "World"]
    HyFI.save_wordlist(words, "workspace/test.txt", sort=False)


def test_load_wordlist():
    words = HyFI.load_wordlist(
        "workspace/test.txt", unique=True, lowercase=True, sort=True
    )
    print(words)
    assert words == ["hello", "world"]
    words = HyFI.load_wordlist(
        "workspace/test.txt", unique=False, lowercase=True, sort=False
    )
    print(words)
    assert words == ["hello", "world", "hello", "world"]
    words = HyFI.load_wordlist(
        "workspace/test.txt", unique=False, lowercase=False, sort=False
    )
    print(words)
    assert words == ["hello", "world", "Hello", "World"]


if __name__ == "__main__":
    test_save_wordlist()
    test_load_wordlist()
