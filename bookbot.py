import argparse

def main():
    parser = argparse.ArgumentParser(
        description="""
            Generates a report on the eBook text whose path is
            specified, showing the number of words and the frequency of
            recurrence for different characters. Desgined to be used
            with a plaintext eBook from Project Gutenberg
            (gutenberg.org).
        """)
    parser.add_argument(
        "-c", "--char_type",
        help="""
            Specifies which characters to include in the report.
            Options: alpha [default], alnum, ascii, numeric
        """,
        nargs=1, default=["alpha"])
    parser.add_argument(
        "-r", "--reverse",
        help="""
            Displays the results in reverse (ascending order if
            sorting by recurrence count or descending order if sorting
            by ASCII code).
        """,
        action="store_false")
    parser.add_argument(
        "-s", "--sort",
        help="""
            Specifies how to sort the results. Options: num [default]
            (by recurrence count), ascii (by ASCII code)
        """,
        nargs=1, default=["num"])
    parser.add_argument(
        "-t", "--trim",
        help="""
            Removes the header and footer added by Project Gutenberg
            from the results, as well as any whitespace lines from the
            beginning and end of the file.
        """,
        action="store_true")
    parser.add_argument(
        "book_path",
        help="""
            The path to a plaintext file. Designed to be a plaintext
            eBook from Project Gutenberg (gutenberg.org).
        """)
    args = parser.parse_args()

    try:
        with open(args.book_path) as f:
            book = f.read()
    except FileNotFoundError:
        print(f"ERROR: '{args.book_path}' does not exist")
        return 1
    except Exception as e:
        print(f"ERROR: unexpected crash\n\t{e}")

    # args.char_type and args.sort are each a list of one argument
    char_type_arg, sort_arg = args.char_type[0], args.sort[0]

    try:
        check_args(char_type_arg, sort_arg, args.book_path)
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    # default to descending order if sorting by recurrence count, or to
    # ascending order if sorting by ascii code
    reverse_arg = args.reverse
    if sort_arg == "ascii":
        reverse_arg = not reverse_arg

    if args.trim:
        book = trim_book(book)
            

    num_words = word_count(book)
    num_chars = character_count(book)
    num_chars = dict_convert_to_list(num_chars)

    if sort_arg == "ascii":
        num_chars.sort(reverse=reverse_arg, key=sort_on_ascii)
    elif sort_arg == "num":
        num_chars.sort(reverse=reverse_arg, key=sort_on_num)

    print(f"--- Begin report of {args.book_path} ---")
    print(f"{num_words} words found in the document\n")
    
    for entry in num_chars:
        line = report_entry(entry, char_type_arg)
        if line != None:
            print(line)

    print("--- End report ---")

# checks validity of command arguments and throws exceptions if
# necessary
def check_args(char_type, sort, book_path):
    if book_path[len(book_path) - 4:] != ".txt":
        raise Exception("'book_path' must be path to .txt file")
    
    if not (char_type == "alpha" or char_type == "alnum" or char_type == "ascii" \
            or char_type == "numeric"):
        raise Exception("invalid argument for flag 'char_type'")
    
    if sort != "num" and sort != "ascii":
        raise Exception("invalid argument for flag 'sort'")

# executes functionality of flag 'trim'
def trim_book(text):
    lines = text.splitlines(keepends=True)
    i = 0

    while i < len(lines) and "*** START OF THE PROJECT GUTENBERG EBOOK" not in lines[i]:
        i += 1

    if i >= len(lines):
        print("WARN: Project Gutenberg header not found")
    else:
        lines = lines[i + 1:]

    i = len(lines) - 1

    while i >= 0 and "*** END OF THE PROJECT GUTENBERG EBOOK" not in lines[i]:
        i -= 1

    if i < 0:
        print("WARN: Project Gutenberg footer not found")
    else:
        lines = lines[:i]

    text = "".join(lines)
    text = text.strip()
    text = text.rstrip()
    return text

# counts number of words in the text
def word_count(text):
    words = text.split()
    return len(words)

# returns a dictionary containing info on the frequency of recurrence
# for each character in the text
def character_count(text):
    text = text.lower()
    char_count = {}

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    return char_count

# converts a dictionary to a list of dictionaries
def dict_convert_to_list(dict):
    new_list = []

    for key in dict:
        new_list.append({"key": key, "value": dict[key]})

    return new_list

# defines the sort key for sorting by number of recurrences
def sort_on_num(dict):
    return dict["value"]

# defines the sort key for sorting by ascii code
def sort_on_ascii(dict):
    return dict["key"]

# generates a report entry for a single character, if that character
# should be part of the report
def report_entry(entry, char_type):
    if char_type == "alnum" and entry["key"].isalnum():
        return f"The '{entry["key"]}' character was found {entry["value"]} times"
    elif char_type == "ascii" and entry["key"].isascii():
        return f"The '{entry["key"]}' character was found {entry["value"]} times"
    elif char_type == "numeric" and entry["key"].isnumeric():
        return f"The '{entry["key"]}' character was found {entry["value"]} times"
    elif char_type == "alpha" and entry["key"].isalpha():
        return f"The '{entry["key"]}' character was found {entry["value"]} times"


main()