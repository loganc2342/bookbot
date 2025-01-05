import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Generates a report on the eBook text whose path is specified, showing the frequency of recurrence for different characters.")
    parser.add_argument(
        "-c", "--char_type",
        help="Specifies which characters to include in the report. Options: alpha [default], alnum, ascii, numeric",
        nargs=1, default=["alpha"])
    parser.add_argument(
        "-r", "--reverse",
        help="Displays the results in reverse (ascending order if sorting by recurrence count or descending order if sorting by ascii code).",
        action="store_false")
    parser.add_argument(
        "-s", "--sort",
        help="Specifies how to sort the results. Options: num [default] (by recurrence count), ascii (by ascii code)",
        nargs=1, default=["num"])
    parser.add_argument(
        "-t", "--trim",
        help="Removes the header and footer added by Project Gutenberg from the results.",
        action="store_true")
    parser.add_argument(
        "book",
        help="The path to a plaintext file. Designed to be a plaintext eBook from Project Gutenberg (gutenberg.org).")
    args = parser.parse_args()

    char_type_arg, sort_arg = args.char_type[0], args.sort[0]

    try:
        check_flags(char_type_arg, sort_arg)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    # default to descending order if sorting by recurrence count, or to ascending order if sorting by ascii code
    reverse_arg = args.reverse
    if sort_arg == "ascii":
        reverse_arg = not reverse_arg

    with open(args.book) as f:
        book_text = f.read()

    num_words = word_count(book_text)
    num_chars = character_count(book_text)
    num_chars = dict_convert_to_list(num_chars)

    if sort_arg == "ascii":
        num_chars.sort(reverse=reverse_arg, key=sort_on_ascii)
    elif sort_arg == "num":
        num_chars.sort(reverse=reverse_arg, key=sort_on_num)

    print(f"--- Begin report of {args.book} ---")
    print(f"{num_words} words found in the document\n")
    
    for entry in num_chars:
        line = report_entry(entry, char_type_arg)
        if line != None:
            print(line)

    print("--- End report ---")


def check_flags(char_type, sort):
    if not (char_type == "alpha" or char_type == "alnum" or char_type == "ascii" or char_type == "numeric"):
        raise Exception("invalid argument for flag 'char_type'")
    
    if sort != "num" and sort != "ascii":
        raise Exception("invalid argument for flag 'sort'")

def word_count(text):
    words = text.split()
    return len(words)

def character_count(text):
    text = text.lower()
    char_count = {}

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    return char_count

def dict_convert_to_list(dict):
    new_list = []

    for key in dict:
        new_list.append({"key": key, "value": dict[key]})

    return new_list

def sort_on_num(dict):
    return dict["value"]

def sort_on_ascii(dict):
    return dict["key"]

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