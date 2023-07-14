import os
from hyfi.utils.envs import ENVs


def test_getcwd():
    assert ENVs.getcwd() == os.getcwd()


def test_find_dotenv():
    print(ENVs.find_dotenv())
    print(os.path.join(os.getcwd(), ".env"))
    assert os.path.exists(ENVs.find_dotenv())


if __name__ == "__main__":
    test_getcwd()
    test_find_dotenv()
