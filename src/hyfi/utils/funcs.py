"""Utility functions for hyfi"""
import ast
import itertools
import re
import sys
from contextlib import suppress
from typing import Any, Dict, List, Optional, TextIO, Type, Union

import chardet
import colorama
from pydantic import StrictBool

from hyfi.utils.types import IntSeq

colorama.init()


class Style:
    """Common color styles."""

    OK: IntSeq = [colorama.Fore.GREEN, colorama.Style.BRIGHT]  # type: ignore
    WARNING: IntSeq = [colorama.Fore.YELLOW, colorama.Style.BRIGHT]  # type: ignore
    IGNORE: IntSeq = [colorama.Fore.CYAN]  # type: ignore
    DANGER: IntSeq = [colorama.Fore.RED, colorama.Style.BRIGHT]  # type: ignore
    RESET: IntSeq = [colorama.Fore.RESET, colorama.Style.RESET_ALL]  # type: ignore


INDENT = " " * 2
HLINE = "-" * 42

NO_VALUE: object = object()


class FUNCs:
    @staticmethod
    def unescape_dict(d):
        """Unescape a dictionary"""
        return ast.literal_eval(repr(d).encode("utf-8").decode("unicode-escape"))

    @staticmethod
    def lower_case_with_underscores(string):
        """Converts 'CamelCased' to 'camel_cased'."""
        return (
            re.sub(r"\s+", "_", re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower())
            .replace("-", "_")
            .replace("__", "_")
        )

    @staticmethod
    def ordinal(num):
        """Return the ordinal of a number as a string."""
        return "%d%s" % (
            num,
            "tsnrhtdd"[(num // 10 % 10 != 1) * (num % 10 < 4) * num % 10 :: 4],
        )

    @staticmethod
    def get_offset_ranges(count, num_workers):
        """Get offset ranges for parallel processing"""
        assert count > num_workers
        step_sz = int(count / num_workers)
        offset_ranges = [0]
        pv_cnt = 1
        for i in range(num_workers):
            pv_cnt = count + 1 if i == num_workers - 1 else pv_cnt + step_sz
            offset_ranges.append(pv_cnt)
        return offset_ranges

    @staticmethod
    def fancy_print(*args, color=None, bold=False, **kwargs):
        """Print with color and bold"""
        if bold:
            print("\033[1m", end="")

        if color:
            print(f"\033[{color}m", end="")

        print(*args, **kwargs)

        print("\033[0m", end="")  # reset

    # https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb/37423778
    @staticmethod
    def humanbytes(B, units=None):
        "Return the given bytes as a human friendly KB, MB, GB, or TB string"
        B = float(B)
        KB = float(1024)
        MB = float(KB**2)  # 1,048,576
        GB = float(KB**3)  # 1,073,741,824
        TB = float(KB**4)  # 1,099,511,627,776

        if (B < KB and units is None) or units == "B":
            return "{0} {1}".format(B, "Bytes" if 0 == B > 1 else "Byte")
        elif (KB <= B < MB and units is None) or units == "KiB":
            return "{0:.2f} KiB".format(B / KB)
        elif (MB <= B < GB and units is None) or units == "MiB":
            return "{0:.2f} MiB".format(B / MB)
        elif (GB <= B < TB and units is None) or units == "GiB":
            return "{0:.2f} GiB".format(B / GB)
        elif (TB <= B and units is None) or units == "TiB":
            return "{0:.2f} TiB".format(B / TB)

    @staticmethod
    def parse_size(sizestr):
        """
        Parse a size string into a number of bytes. For example, "16K" will
        return 16384.  If no suffix is provided, bytes are assumed.  This
        function is case-insensitive.

        :param sizestr: A string representing a size, such as "16K", "2M", "1G".
        :return: The number of bytes that the string represents.
        """
        unit = sizestr[-1]
        size = float(sizestr[:-1])

        if unit.upper() == "B":
            return size
        if unit.upper() == "K":
            return size * 1024
        if unit.upper() == "M":
            return size * 1024 * 1024
        if unit.upper() == "G":
            return size * 1024 * 1024 * 1024
        if unit.upper() == "T":
            return size * 1024 * 1024 * 1024 * 1024

    @staticmethod
    def check_min_len(s, len_func, min_len):
        """Check if the length of a string is greater than or equal to a minimum length"""
        return len_func(s) >= min_len

    @staticmethod
    def check_max_len(s, len_func, max_len):
        """Check if the length of a string is less than or equal to a maximum length"""
        return len_func(s) <= max_len

    @staticmethod
    def utf8len(s):
        """Return the length of a string in bytes"""
        return len(str(s).encode("utf-8"))

    @staticmethod
    def len_wospc(x):
        """Return the length of a string in bytes without spaces"""
        return FUNCs.utf8len(re.sub(r"\s", "", str(x)))

    @staticmethod
    def len_bytes(x):
        """Return the length of a string in bytes"""
        return FUNCs.utf8len(x)

    @staticmethod
    def len_words(x):
        """Return the number of words in a string"""
        return len(x.split()) if isinstance(x, str) else 0

    @staticmethod
    def len_sents(x, sep):
        """Return the number of sentences in a string"""
        sep = str(sep).encode("utf-8").decode("unicode-escape")
        return len(re.sub(r"(\r?\n|\r){1,}", sep, x).split(sep))

    @staticmethod
    def len_segments(x, sep):
        """Return the number of segments in a string"""
        sep = str(sep).encode("utf-8").decode("unicode-escape")
        return len(re.sub(r"(\r?\n|\r){2,}", sep, x).split(sep))

    @staticmethod
    def any_to_utf8(b):
        """Convert any string to utf-8"""
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError:
            # try to figure out encoding if not utf-8

            guess = chardet.detect(b)["encoding"]

            if not guess or guess == "UTF-8":
                return

            try:
                return b.decode(guess)
            except (UnicodeDecodeError, LookupError):
                # still cant figure out encoding, give up
                return

    @staticmethod
    def today(_format="%Y-%m-%d"):
        """Return today's date"""
        from datetime import datetime

        if _format is None:
            return datetime.today().date()
        else:
            return datetime.today().strftime(_format)

    @staticmethod
    def now(_format="%Y-%m-%d %H:%M:%S"):
        """Return current date and time"""
        from datetime import datetime

        return datetime.now() if _format is None else datetime.now().strftime(_format)

    @staticmethod
    def strptime(
        _date_str: str,
        _format: str = "%Y-%m-%d",
    ):
        """Return a datetime object from a string"""
        from datetime import datetime

        return datetime.strptime(_date_str, _format)

    @staticmethod
    def to_dateparm(_date, _format="%Y-%m-%d"):
        """Return a date parameter string"""
        from datetime import datetime

        _dtstr = datetime.strftime(_date, _format)
        _dtstr = "${to_datetime:" + _dtstr + "," + _format + "}"
        return _dtstr

    @staticmethod
    def human_readable_type_name(t: Type) -> str:
        """
        Generates a useful-for-humans label for a type.
        For builtin types, it's just the class name (eg "str" or "int").
        For other types, it includes the module (eg "pathlib.Path").
        """
        module = t.__module__
        if module == "builtins":
            return t.__qualname__
        elif module.split(".")[0] == "hyfi":
            module = "hyfi"

        try:
            return f"{module}.{t.__qualname__}"
        except AttributeError:
            return str(t)

    @staticmethod
    def readable_types_list(type_list: List[Type]) -> str:
        """Generates a useful-for-humans label for a list of types."""
        return ", ".join(FUNCs.human_readable_type_name(t) for t in type_list)

    @staticmethod
    def dict_product(dicts) -> List[Dict]:
        """
        >>> list(dict_product(dict(number=[1,2], character='ab')))
        [{'character': 'a', 'number': 1},
        {'character': 'a', 'number': 2},
        {'character': 'b', 'number': 1},
        {'character': 'b', 'number': 2}]
        """
        return [dict(zip(dicts, x)) for x in itertools.product(*dicts.values())]

    @staticmethod
    def printf(
        action: str,
        msg: Any = "",
        style: Optional[IntSeq] = None,
        indent: int = 10,
        verbose: Union[bool, StrictBool] = True,
        file_: TextIO = sys.stdout,
    ) -> Optional[str]:
        """Print string with common format."""
        if not verbose:
            return None  # HACK: Satisfy MyPy
        _msg = str(msg)
        action = action.rjust(indent, " ")
        if not style:
            return action + _msg

        out = style + [action] + Style.RESET + [INDENT, _msg]  # type: ignore
        print(*out, sep="", file=file_)
        return None  # HACK: Satisfy MyPy

    @staticmethod
    def printf_exception(
        e: Exception, action: str, msg: str = "", indent: int = 0, quiet: bool = False
    ) -> None:
        """Print exception with common format."""
        if not quiet:
            print("", file=sys.stderr)
            FUNCs.printf(
                action, msg=msg, style=Style.DANGER, indent=indent, file_=sys.stderr
            )
            print(HLINE, file=sys.stderr)
            print(e, file=sys.stderr)
            print(HLINE, file=sys.stderr)

    @staticmethod
    def cast_str_to_bool(value: Any) -> bool:
        """Parse anything to bool.

        Params:
            value:
                Anything to be casted to a bool. Tries to be as smart as possible.

                1.  Cast to number. Then: 0 = False; anything else = True.
                1.  Find [YAML booleans](https://yaml.org/type/bool.html),
                    [YAML nulls](https://yaml.org/type/null.html) or `none` in it
                    and use it appropriately.
                1.  Cast to boolean using standard python `bool(value)`.
        """
        # Assume it's a number
        with suppress(TypeError, ValueError):
            return bool(float(value))
        # Assume it's a string
        with suppress(AttributeError):
            lower = value.lower()
            if lower in {"y", "yes", "t", "true", "on"}:
                return True
            elif lower in {"n", "no", "f", "false", "off", "~", "null", "none"}:
                return False
        # Assume nothing
        return bool(value)

    @staticmethod
    def force_str_end(original_str: str, end: str = "\n") -> str:
        """Make sure a `original_str` ends with `end`.

        Params:
            original_str: String that you want to ensure ending.
            end: String that must exist at the end of `original_str`
        """
        return original_str if original_str.endswith(end) else original_str + end
