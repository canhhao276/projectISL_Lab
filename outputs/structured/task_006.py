import re

class AutomaticGuitarSimulator:
    def __init__(self, text) -> None:
        """
        Initialize the score to be played
        :param text:str, score to be played
        """
        self.play_text = text

    def interpret(self, display=False):
        """
        Interpret the music score to be played
        :param display:Bool, representing whether to print the interpreted score
        :return: list of dict, The dict includes two fields, Chord and Tune, which are letters and numbers, respectively. If the input is empty or contains only whitespace, an empty list is returned.
        """
        if not self.play_text or not self.play_text.strip():
            return []

        # Regex to split chord (letters) and tune (numbers)
        # Matches letters followed by numbers
        pattern = r'([A-Za-z]+)(\d+)'
        matches = re.findall(pattern, self.play_text)
        
        result = []
        for chord, tune in matches:
            item = {'Chord': chord, 'Tune': tune}
            result.append(item)
            if display:
                self.display(chord, tune)
        
        return result

    def display(self, key, value):
        """
        Print out chord and play tune with following format: Normal Guitar Playing -- Chord: %s, Play Tune: %s
        :param key:str, chord
        :param value:str, play tune
        :return: str
        """
        output = f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"
        print(output)
        return output