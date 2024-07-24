import argparse
import glob
import os
from textwrap import indent, dedent

import yara
from tabulate import tabulate

__version__ = "1.0.0"


class YaraGrep():
    def __init__(self, _strings, _bytes, _any=False, _modifier="", _quiet=False):
        if not _strings and not _bytes:
            raise ValueError(
                "At least one 'string' or 'bytes' pattern required")

        self.verbose = not _quiet
        patterns = "\n"
        condition = "any of them" if _any else "all of them"

        for i, fragment in enumerate(_strings):
            patterns += f"$s{i} = \"{fragment}\" {_modifier}\n"

        for i, fragment in enumerate(_bytes):
            patterns += f"$b{i} = {{ {fragment} }}\n"

        rule = dedent(f"""\
        rule x {{
            strings:{indent(patterns.rstrip(), " " * 16)}
            condition:
                {condition}
        }}
        """)

        print(rule)
        self.rule = yara.compile(source=rule)

    def scan(self, path):
        for filename in glob.glob(path, recursive=True):
            if not os.path.isfile(filename):
                continue
            try:
                matches = self.rule.match(filename)
            except yara.Error as e:
                if self.verbose:
                    print(e)
                continue

            if matches:
                print(filename)
                if self.verbose:
                    table = [[hex(offset), repr(pattern), pattern.hex(" ")]
                             for offset, _, pattern in matches[0].strings]
                    print(tabulate(table))


def main():
    parser = argparse.ArgumentParser(
        description="yara grep - cmdline string/byte search")
    parser.add_argument("path", nargs="?", default="**",
                        help="search path (default: **)")
    parser.add_argument("-l", "--quiet", action="store_true",
                        default=False, help="list matching filenames only (suppress normal output)")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="do not scan, compile rule only")
    parser.add_argument("-a", "--any", action="store_true",
                        default=False, help="set condition to 'any of them' (default: 'all of them')")
    parser.add_argument("-m", "--modifier", default="ascii wide nocase",
                        help="modifier for string patterns - e.g. ascii,wide,nocase,xor,base64,base64wide")
    parser.add_argument("-b", "--bytes", help="bytes to grep",
                        action="append", default=[])
    parser.add_argument("-s", "--string", help="string to grep",
                        action="append", default=[])

    args = parser.parse_args()
    yara_grep = YaraGrep(args.string, args.bytes,
                         args.any, args.modifier, args.quiet)
    if not args.dry_run:
        yara_grep.scan(args.path)


if __name__ == "__main__":
    main()
