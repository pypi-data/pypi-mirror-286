import re
import bitmath


def parse_size(sentence):
    """
    Parses the sizes from a sentence and returns them in bytes.

    Args:
        sentence (str): The sentence containing sizes to be parsed.

    Returns:
        list: A list of sizes in bytes.

    """
    # Regular expression pattern for a size
    pattern = r'\b\d+(\.\d+)?\s*[KkMmGgTtPpEeZzYy]?[i]?[Bb]?\b'
    
    # Find all sizes in the sentence
    matches = re.findall(pattern, sentence)
    
    sizes = []
    for match in matches:
        try:
            # Parse the size to a bitmath object
            size = bitmath.parse_string(match)
            
            # Convert the size to bytes and return
            sizes.append(size.to_Byte().value)
        except ValueError:
            pass  # Ignore sizes that can't be parsed
    
    return sizes
