from typing import List

class RegexEngine:
    """
    RegexEngine is a class that compiles and manages a set of regular expression patterns.

    Attributes:
        raw_patterns (List[str]): A list of raw patterns as strings.
        compiled_patterns (List[re.Pattern]): A list of compiled regex patterns.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of RegexEngine.
        
        The `raw_patterns` attribute is initialized as an empty list to store raw regex patterns.
        The `compiled_patterns` attribute is initialized as an empty list to store compiled regex patterns.
        """
        ...

    def add_patterns(self, patterns: List[str], escape: bool) -> int:
        """
        Adds a list of patterns to the RegexEngine object. The patterns are compiled and stored in the object.

        Args:
            patterns (List[str]): A list of raw regex patterns to compile.
            escape (bool): A boolean flag to escape the patterns before compiling.

        Returns:
            int: The number of patterns that were successfully compiled.
        """
        ...
        
    @property
    def raw_patterns(self) -> List[str]:
        """
        Returns the raw patterns that were compiled.

        Returns:
            List[str]: A list of raw patterns that were compiled. The order of the patterns is the same as the order of the compiled patterns. The indexes of the raw patterns and the compiled patterns match.
        """
        ...

    def search(self, content: str) -> List[int]:
        """
        Runs the compiled patterns against the provided content.

        Args:
            content (str): The content to match against.

        Returns:
            List[int]: A list of indexes of the patterns that matched the content.
        """
        ...