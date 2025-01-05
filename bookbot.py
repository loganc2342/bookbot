import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Generates a report on the eBook text whose path is specified, showing the frequency of recurrence for different characters.")
    parser.add_argument(
        "-c", "--char_type",
        help="Specifies which characters to include in the report. Options: alpha [default], alnum, ascii, numeric",
        nargs=1, default="alpha")
    parser.add_argument(
        "-r", "--reverse",
        help="Displays the results in ascending order.",
        action="store_true")
    parser.add_argument(
        "-s", "--sort",
        help="Specifies how to sort the results. Options: num [default] (by recurrence count), ascii (by ascii code)",
        nargs=1, default="num")
    parser.add_argument(
        "-t", "--trim",
        help="Removes the header and footer added by Project Gutenberg from the results.",
        action="store_true")
    parser.add_argument(
        "book",
        help="The path to a plaintext file. Designed to be a plaintext eBook from Project Gutenberg (gutenberg.org).")
    args = parser.parse_args()
    book = args.book

    with open(book) as f:
        book_text = f.read()

    num_words = word_count(book_text)
    num_chars = character_count(book_text)
    num_chars = dict_convert_to_list(num_chars)
    num_chars.sort(reverse=True, key=sort_on)

    print(f"--- Begin report of {book} ---")
    print(f"{num_words} words found in the document\n")

    for entry in num_chars:
        if entry["key"].isalpha():
            print(f"The '{entry["key"]}' character was found {entry["value"]} times")

    print("--- End report ---")
    
# Flags: --help, --type=alpha (alnum, ascii, numeric), -r (--remove, removes header), --sort=num (ascii)

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

def sort_on(dict):
    return dict["value"]


main()