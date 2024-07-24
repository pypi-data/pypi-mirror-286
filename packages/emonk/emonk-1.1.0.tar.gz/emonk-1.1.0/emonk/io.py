from datetime import datetime
import os
import sys

from . import config
from . import crypto
from . import dialog

ISO_FORMAT = "%Y-%m-%d %H:%M"


def join(d, custom_format=False):
    """Join datestamp: entry dict into string.

    Args:
        d (dict): dictionary of journal entries.
        custom_format (bool): use custom date format.

    Returns:
        journal entries as a string.
    """
    s = ""
    for key in sorted(d.keys()):
        body = d[key].strip()
        # Drop blank journal entries.
        if not body:
            continue
        if custom_format:
            date = iso2custom(key)
        else:
            date = key
        s += f"{date}\n{body}\n\n"
    return s


def read_stdin():
    """If stdin has text, import it and exit.

    Example:
        emonk < file.txt
    """
    # Don't lock console!
    os.set_blocking(0, False)
    s = "".join(sys.stdin.readlines())
    if s:
        d = read()
        imported = split(s)
        d.update(imported)
        write(d)
        print(f"Imported {len(imported.keys())} entries.")
        sys.exit()


def split(s, custom_format=False):
    """Split string s into dictionary.

    Args:
        s (str): journal entries.
        custom_format (bool): use custom date format.

    Returns:
        dict: datestamp:entry string.
    """
    d = {}
    key = None
    if custom_format:
        date_format = config.get("date_format", ISO_FORMAT)
    else:
        date_format = ISO_FORMAT
    for line in s.splitlines():
        line = line.strip()
        if is_timestamp(line, date_format):
            if custom_format:
                key = custom2iso(line)
            else:
                key = line
            d[key] = ""
        else:
            if key:
                d[key] += line + "\n"
    return {key: val.strip() for key, val in d.items()}


def read():
    """Read journal file and convert to dictionary.

    Note:
        The journal file datestamps and dictionary keys use ISO format. This
        allows for easy sorting by date, and easy conversion to a custom
        datetime format.

    Returns:
        dict: datestamp:entry string.
    """
    try:
        if config.get("encrypt"):
            with open(config.get("path"), "rb") as f:
                b = f.read()
            pw = dialog.input_password()
            s = crypto.decrypt(b, pw)
        else:
            with open(config.get("path")) as f:
                s = f.read()
        return split(s)
    except FileNotFoundError:
        return {}


def write(d):
    """Convert dictionary to string and write to journal file."""
    s = join(d)
    if config.get("encrypt"):
        b = crypto.encrypt(s)
        with open(config.get("path"), "wb") as f:
            f.write(b)
    else:
        with open(config.get("path"), "w") as f:
            f.write(s)


def is_timestamp(s, date_format):
    try:
        datetime.strptime(s.strip(), date_format)
        return True
    except:
        return False


def iso2custom(s):
    """Convert datetime string s from ISO to custom date format."""
    date_format = config.get("date_format", ISO_FORMAT)
    return datetime.strptime(s, "%Y-%m-%d %H:%M").strftime(date_format)


def custom2iso(s):
    """Convert datetime string s from custom to ISO date format."""
    date_format = config.get("date_format", ISO_FORMAT)
    return datetime.strptime(s, date_format).strftime("%Y-%m-%d %H:%M")
