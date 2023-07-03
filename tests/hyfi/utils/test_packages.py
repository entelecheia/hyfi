import os
import shutil
import tempfile
import unittest

from hyfi.utils.packages import PKGs


class TestPKGs(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_gitclone(self):
        url = "https://github.com/entelecheia/hello.git"
        targetdir = os.path.join(self.temp_dir, "hello")
        PKGs.gitclone(url, targetdir)
        self.assertTrue(os.path.exists(targetdir))

    # def test_load_module_from_file(self):
    #     name = "mymodule"
    #     libpath = os.path.join(self.temp_dir, "mymodule")
    #     with open(libpath, "w") as f:
    #         f.write("def myfunc():\n    return 'hello'")
    #     PKGs.load_module_from_file(name, libpath)
    #     self.assertTrue(hasattr(mymodule, "myfunc"))

    # def test_ensure_import_module(self):
    #     name = "mymodule"
    #     libpath = os.path.join(self.temp_dir, "mymodule")
    #     liburi = "https://github.com/username/repo.git"
    #     PKGs.ensure_import_module(name, libpath, liburi)
    #     self.assertTrue(hasattr(mymodule, "myfunc"))

    def test_getsource(self):
        source = PKGs.getsource("os.path.join")
        self.assertTrue("def join(a, *p):" in source)

    def test_viewsource(self):
        PKGs.viewsource("os.path.join")
        # should print the source code of os.path.join
