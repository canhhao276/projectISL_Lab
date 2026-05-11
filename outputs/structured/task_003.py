class ArgumentParser:
    """
    This is a class for parsing command line arguments to a dictionary.
    """

    def __init__(self):
        """
        Initialize the fields.
        self.arguments is a dict that stores the args in a command line
        self.requried is a set that stores the required arguments
        self.types is a dict that stores type of every arguments.
        """
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        """
        Parses the given command line argument string and invoke _convert_type to stores the parsed result in specific type in the arguments dictionary.
        Checks for missing required arguments, if any, and returns False with the missing argument names, otherwise returns True.
        """
        parts = command_string.split()[2:]  # Skip "python script.py"
        i = 0
        while i < len(parts):
            part = parts[i]
            if part.startswith('-'):
                key = part.lstrip('-')
                if '=' in key:
                    key, value = key.split('=', 1)
                    self.arguments[key] = self._convert_type(key, value)
                elif i + 1 < len(parts) and not parts[i + 1].startswith('-'):
                    self.arguments[key] = self._convert_type(key, parts[i + 1])
                    i += 1
                else:
                    self.arguments[key] = True
            i += 1

        missing_args = self.required - set(self.arguments.keys())
        if missing_args:
            return (False, missing_args)
        return (True, None)

    def get_argument(self, key):
        """
        Retrieves the value of the specified argument from the arguments dictionary and returns it.
        """
        return self.arguments.get(key)

    def add_argument(self, arg, required=False, arg_type=str):
        """
        Adds an argument to self.types and self.required.
        """
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def _convert_type(self, arg, value):
        """
        Try to convert the type of input value by searching in self.types.
        """
        if arg in self.types:
            target_type = self.types[arg]
            try:
                if target_type == 'int':
                    return int(value)
                elif target_type == 'float':
                    return float(value)
                elif target_type == 'bool':
                    return value.lower() in ('true', '1', 'yes')
                return target_type(value)
            except (ValueError, TypeError):
                return value
        return value