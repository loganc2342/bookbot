# bookbot
BookBot is my first project!

In its original form—the form submitted as a project for [Boot.dev](https://www.boot.dev/tracks/backend)—the
BookBot took a hard-coded path to a plaintext file and generated a report showing the number of words and the
frequency of recurrence for each letter. I've modified it so it now takes command line arguments, including:

* `book_path`: The path to a .txt file.
* `-c`, `--char_type`: A filter to include different characters in the report besides just letters.
* `-n`, `--no_lower`: Has the report treat uppercase and lowercase letter as separate characters.
* `-r`, `--reverse`: Reverses the order of the results.
* `-s`, `--sort`: Allows for sorting of the results by ASCII code, rather than just by recurrence count.
* `-t`, `--trim`: Removes leading and trailing whitespace from the textfile, as well as the header
                  and footer provided by Project Gutenberg to their eBooks.

The BookBot is designed to be used with eBooks in the form of plaintext files, downloaded from the website of [Project Gutenberg](https://gutenberg.org/).