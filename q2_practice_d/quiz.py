# No imports!


#############
# Problem 1 #
#############

def ascending_path(graph, start, end):
    raise NotImplementedError


#############
# Problem 2 #
#############

allwords = set(open('words2.txt').read().splitlines())

def is_word(i):
    return i.lower() in allwords

key_letters = {
    '2': 'ABC',
    '3': 'DEF',
    '4': 'GHI',
    '5': 'JKL',
    '6': 'MNO',
    '7': 'PQRS',
    '8': 'TUV',
    '9': 'WXYZ',
}

def phone_words(digits):
    raise NotImplementedError


#############
# Problem 3 #
#############

class MITube:
    """MIT's video sharing platform."""

    def __init__(self):
        """
        Initializes an empty MITube instance with no videos.
        """
        raise NotImplementedError

    def upload_video(self, title, username):
        """
        Adds a new MITube video (with 0 views).

        Args:
            title: title of the video being added (string)
            username: username of the MITuber adding the video (string)
        """
        raise NotImplementedError

    def view(self, title):
        """
        Increments the view count for the video with given title.

        Args:
            title: title of video being viewed (string)
        Raises:
            ValueError if video has not been uploaded
        """
        raise NotImplementedError

    def get_top_video(self):
        """
        Finds the best video, where "best" is defined as the video having the
        most views, with ties broken by alphabetical ordering by title.

        Returns:
            title of the best video (string)
        """
        raise NotImplementedError

    def get_top_user(self):
        """
        Finds the best MITuber, where "best" is defined as the MITuber having
        the most cumulative views, with ties broken by alphabetical ordering
        by username.

        Returns:
            username of the best MITuber (string)
        """
        raise NotImplementedError


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
