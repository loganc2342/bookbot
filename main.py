def main():
    book = "books/frankenstein.txt"
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