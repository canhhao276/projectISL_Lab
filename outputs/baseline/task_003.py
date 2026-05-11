class ArgumentParser:
    """
    This is a class for parsing command line arguments to a dictionary.
    """

    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        parts = command_string.split()[2:]  # Skip "python script.py"
        i = 0
        while i < len(parts):
            part = parts[i]
            if part.startswith('-'):
                # Handle --key=value or -key=value
                if '=' in part:
                    key, value = part.lstrip('-').split('=', 1)
                    self.arguments[key] = self._convert_type(key, value)
                else:
                    key = part.lstrip('-')
                    # Check if next part is a value or another flag
                    if i + 1 < len(parts) and not parts[i + 1].startswith('-'):
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
        return self.arguments.get(key)

    def add_argument(self, arg, required=False, arg_type=str):
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def _convert_type(self, arg, value):
        if arg in self.types:
            target_type = self.types[arg]
            try:
                if target_type == 'int' or target_type == int:
                    return int(value)
                elif target_type == 'float' or target_type == float:
                    return float(value)
                elif target_type == 'bool' or target_type == bool:
                    return value.lower() in ('true', '1', 'yes')
            except ValueError:
                return value
        return value