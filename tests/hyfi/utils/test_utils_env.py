import unittest
from hyfi.utils.envs import ENVs


class TestExpandPosixVars(unittest.TestCase):
    def test_expand_posix_vars(self):
        # Test expanding $PWD and $USER variables
        posix_expr = "The current working directory is $PWD and the user is $USER."
        expanded_expr = ENVs.expand_posix_vars(posix_expr)
        self.assertIn("The current working directory is", expanded_expr)
        self.assertIn("and the user is", expanded_expr)

        # Test expanding custom variable
        posix_expr = "The value of MY_VAR is $MY_VAR."
        context = {"MY_VAR": "hello world"}
        expanded_expr = ENVs.expand_posix_vars(posix_expr, context)
        self.assertIn("The value of MY_VAR is", expanded_expr)
        self.assertIn("hello world", expanded_expr)

        # Test expanding non-existent variable
        posix_expr = "The value of NON_EXISTENT_VAR is $NON_EXISTENT_VAR."
        expanded_expr = ENVs.expand_posix_vars(posix_expr)
        self.assertIn("The value of NON_EXISTENT_VAR is", expanded_expr)
        self.assertIn("", expanded_expr)


if __name__ == "__main__":
    unittest.main()
