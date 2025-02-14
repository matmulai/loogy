```python
from typing import Dict, Optional

def search_word_in_dictionary(dictionary: Dict[str, str], word: str) -> Optional[str]:
    """
    Searches for a word in the given dictionary.

    Parameters:
    dictionary (Dict[str, str]): A dictionary where keys are words and values are their definitions.
    word (str): The word to search for in the dictionary.

    Returns:
    Optional[str]: The definition of the word if found, otherwise None.
    """
    # Normalize the word to lower case for case-insensitive search
    normalized_word = word.lower()
    
    # Search for the word in the dictionary
    definition = dictionary.get(normalized_word)

    return definition

# Example usage
if __name__ == "__main__":
    # Sample dictionary
    sample_dictionary = {
        "python": "A high-level programming language.",
        "javascript": "A scripting language commonly used in web development.",
        "java": "A high-level, class-based, object-oriented programming language."
    }
    
    # Searching for a word
    word_to_search = "Python"
    result = search_word_in_dictionary(sample_dictionary, word_to_search)

    if result:
        print(f"The definition of '{word_to_search}' is: {result}")
    else:
        print(f"The word '{word_to_search}' was not found in the dictionary.")
```

This code defines a function that searches for a particular word in a given dictionary and returns its definition. The function is case-insensitive and handles scenarios where the word is not found by returning `None`. The code also includes an example usage section to show how the function can be utilized in practice.