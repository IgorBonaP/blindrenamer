from random import choice as randc
from string import ascii_letters


def randomstring(length: int)-> str:
    ''' Generates a random string of ASCII letters with a given length'''
    string = "".join(randc(ascii_letters) for m in range(length))
    return string


def capture_except(input_string: str, except_flag: str)-> str:
    ''' Method for stripping a given flag from a string and getting the
    glued pieces as one string

    Example usage:
        - inputstring = somethingAflaginBetweenelse
        - except_flag = AflaginBetween
        Result - > somethingelse
    '''
    if not isinstance(input_string, str) or not isinstance(except_flag, str):
        raise TypeError("Input values must be of type String only")

    split_string = input_string.split(except_flag)
    result = ""
    for words in split_string:
        result += words
    return result


if __name__ == "__main__":
    print(len(ascii_letters))
