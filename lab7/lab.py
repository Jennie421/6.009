# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self, key_type):
        self.value = None
        self.key_type = key_type
        self.children = dict()


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        >>> t = Trie(str)
        >>> t['bat'] = 7
        >>> t['bark'] = ':)'
        >>> t['bar'] = 3
        """
        if type(key) != self.key_type:
            raise TypeError

        if self.key_type == tuple:
            k = (key[0],)
        else:
            k = key[0]

        if k not in self.children:
                self.children[k] = Trie(self.key_type)

        child = self.children[k]
        if len(key) == 1:
            child.value = value
        else:
            child[key[1:]] = value


    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        >>> t = Trie(str)
        >>> t['bat'] = 7 
        >>> t['bat']
        7
        """
        if type(key) != self.key_type:
            raise TypeError
        
        if len(key) == 0:
            raise KeyError('key len is zero')

        if self.key_type == tuple:
            k = (key[0],)
        else:
            k = key[0]

        if k not in self.children:
            raise KeyError
        
        child = self.children[k]

        if len(key) == 1:
            if child.value == None:
                raise KeyError
            else:
                return child.value
        else:
            return child[key[1:]]
        
    
    def getnode(self, key):
        """
        """
        if type(key) != self.key_type:
            raise TypeError
        
        # if len(key) == 0:
        #     return None
        if len(key) == 0:
            return self

        if self.key_type == tuple:
            k = (key[0],)
        else:
            k = key[0]

        if k not in self.children:
            return None

        child = self.children[k]
        if len(key) == 1:
            return child
        else:
            return child.getnode(key[1:])


    def getvalue(self, key):
        if type(key) != self.key_type:
            raise TypeError
        
        if len(key) == 0:
            return self.value

        if self.key_type == tuple:
            k = (key[0],)
        else:
            k = key[0]

        if k not in self.children:
            return None

        child = self.children[k]
        if len(key) == 1:
            return child.value
        else:
            return child.getvalue(key[1:])


    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        >>> t = Trie(str)
        >>> t['bat'] = 7 
        >>> del t['bat']
        >>> 'bat' in t
        False
        """
        if type(key) != self.key_type:
            raise TypeError
        if len(key) == 0:
            raise KeyError('key len is zero')

        if self.key_type == tuple:
            k = (key[0],)
        else:
            k = key[0]

        if k not in self.children:
            raise KeyError

        child = self.children[k]
        if len(key) == 1:
            if child.value == None:
                raise KeyError
            else:
                child.value = None
        else:
            del child[key[1:]]


    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        >>> t = Trie(str)
        >>> t['bar'] = 7 
        >>> 'bar' in t
        True
        >>> 'ba' in t
        False
        >>> 'barking' in t
        False 
        """
        if type(key) != self.key_type:
            raise TypeError

        if len(key) == 0:
            return False
        
        if self.key_type == tuple:
            k = (key[0],)
        else:
            k = key[0]

        if k not in self.children:
            return False
    
        child = self.children[k]
        if len(key) == 1:
            if child.value == None: 
                return False
            return True
        else:
            return key[1:] in child


    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        >>> t = Trie(str)
        >>> t['bat'] = 7
        >>> t['bark'] = ':)'
        >>> t['bar'] = 3
        >>> list(t)
        [('bat', 7), ('bar', 3), ('bark', ':)')]
        """
        if self.value is not None:
            yield (prefix, self.value)
        for prefix, child in self.children.items():
            # if child.value is not None:
            #     yield (prefix, child.value)
            for key, value in child:
                yield (prefix+key, value)


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    >>> t = make_word_trie("bat bat bark bar")
    >>> t['bat']
    2
    >>> t['bark']
    1
    >>> 'ba' in t
    False
    """
    t = Trie(str)
    sentences = tokenize_sentences(text)
    for s in sentences:
        words = s.split(' ') # list of words in a sentence 
        for w in words:
            if w not in t:
                t[w] = 1
            else:
                t[w] += 1
    return t


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    >>> t = make_phrase_trie("I like. you like. I like")
    >>> t['i', 'like']
    2
    >>> t['you',]
    Traceback (most recent call last):
    ...
    KeyError
    """
    t = Trie(tuple)
    sentences = tokenize_sentences(text)
    for s in sentences:
        # convert into tuples of words 
        words = s.split(' ')
        tuple_s = tuple(words)
        if tuple_s not in t:
            t[tuple_s] = 1
        else:
            t[tuple_s] += 1
    return t


def add_prefix(result, prefix):
    """
    for a given list of keys, add the prefix (string or tuple) to every key
    """
    new = []
    for k in result:
        if k != prefix:
            new_k = prefix + k
            new.append(new_k)
        else:
            new.append(k)
    return new 

def only_keys(kvpair):
    keys = []
    for key, value in kvpair:
        keys.append(key) # only keys
    return keys

def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    >>> t = make_word_trie("bat bat bark bar")
    >>> autocomplete(t, "ba", 1)
    ['bat']
    >>> autocomplete(t, "ba", 2) in [['bat', 'bar'], ['bat', 'bark']]
    True 
    >>> autocomplete(t, "be", 2)
    []
    >>> autocomplete(t, 'bar', 1)
    ['bar']
    >>> t = make_phrase_trie("like summer. like winter. like summer. love spring")
    >>> autocomplete(t, ("like",), 1)
    [('like', 'summer')]
    >>> autocomplete(t, ("love",), 2)
    [('love', 'spring')]
    """
    if type(prefix) != trie.key_type:
        raise TypeError
    
    start = trie.getnode(prefix)

    if start == None and (prefix == '' or prefix == tuple()): # if prefix is not in the trie
        no_prefix_pair = set(list(trie))
    elif start == None:
        return []
    else:
        no_prefix_pair = set(list(start))
    
    if start is not None and start.value is not None:
        no_prefix_pair.add((prefix, start.value)) # include the prefix if it exists 

    no_prefix_pair = sorted(no_prefix_pair, key=lambda x: x[1], reverse=True)

    no_prefix = only_keys(no_prefix_pair)

    # full_result = []

    # full_result.extend(add_prefix(no_prefix, prefix))

    full_result = add_prefix(no_prefix, prefix)

    # If there are fewer than max_count valid keys available starting with prefix
    # If max_count is not specified
    if max_count == None or len(full_result) <= max_count:
        return full_result 

    # Return a list of the max_count most-frequently-occurring keys that start with prefix. 
    return full_result[:max_count]



# Helper Functions for autocorrect 

alphabet = [chr(i) for i in range(97, 123)]
def insertion(w):
    """
    A single-character insertion (add any one character in the range "a" to "z" at any place in the word)
    """
    possible = set()
    for letter in alphabet:
        possible |= {w[:ix] + letter + w[ix:] for ix in range(len(w)+1)}
    return possible
   
def deletion(w):
    """
    A single-character deletion (remove any one character from the word)
    """
    possible = set()
    possible |= {w[:ix-1] + w[ix:] for ix in range(1, len(w)+1)}
    return possible

def replacement(w):
    """
    A single-character replacement (replace any one character in the word with a character in the range a-z)
    """
    possible = set()
    for letter in alphabet:
        possible |= {w[:ix-1] + letter + w[ix:] for ix in range(1, len(w)+1)}
    return possible

def transposition(w): 
    """
    A two-character transpose (switch the positions of any two adjacent characters in the word)
    """
    possible = set()
    for i in range(len(w)-1):
        pre = w[:i]
        first = w[i] 
        second = w[i+1]
        rest = w[i+2:]
        possible |= {pre + second + first + rest}
    return possible


def add_prefix_to_words(t, prefix):
    """
    for a given a list of tuple (word, freq), add the prefix (string) to every key
    """
    assert isinstance(prefix, str)
    new = []
    for word, freq in t:
        new_w = prefix + word
        new.append((new_w, freq))
    return new


def valid_edits(trie, prefix):

    valid_edit_pair = set()
    
    possible_prefix = set().union(insertion(prefix), deletion(prefix), replacement(prefix), transposition(prefix))

    for p in possible_prefix:
        start_node = trie.getnode(p)
        if start_node is not None and start_node.value is not None:
            valid_edit_pair |= {(p, trie[p])}

    # sort keys in order from high freq to low freq
    valid_edit_pair = sorted(valid_edit_pair, key=lambda x: x[1], reverse=True)

    # only keys 
    valid = only_keys(valid_edit_pair)

    return valid


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    >>> t = make_word_trie("bat bat bark bar")
    >>> autocorrect(t, "bar", 3) 
    ['bar', 'bark', 'bat']

    >>> t = make_word_trie("Near an era, a nearer ear, a nearly eerie ear, i can")
    >>> sorted(autocorrect(t, "ear", 3)) 
    ['ear', 'era', 'near']
    >>> sorted(autocorrect(t, "an", 3)) 
    ['a', 'an', 'can']
    >>> sorted(autocorrect(t, "a"))
    ['a', 'an', 'i'] 
    >>> sorted(autocorrect(t, "nearl"))
    ['near', 'nearly']
    """
    # autocorrect should invoke autocomplete.
    result = autocomplete(trie, prefix, max_count)
    edits = valid_edits(trie, prefix)
    # print("result = ", result)
    # print('edit = ', edits)

    # If max_count is unspecified, return all autocompletions as well as all valid edits.
    if max_count == None:
        return result + [i for i in edits if i not in result]

    if max_count <= len(result):
        return result[:max_count]

    # if fewer than max_count completions are made, suggest additional words by applying one valid edit to the prefix.
    res = result[:]
    while len(res) < max_count:
        if len(edits) == 0: break 
        new = edits.pop(0)
        if new not in res:
            res.append(new)
    return res


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    >>> t = make_word_trie("bat bat bark bar")
    >>> word_filter(t, "*") 
    [('bat', 2), ('bar', 1), ('bark', 1)]
    >>> word_filter(t, "???") 
    [('bat', 2), ('bar', 1)]
    >>> word_filter(t, "*r*") 
    [('bar', 1), ('bark', 1)]
    >>> t = make_word_trie("sing, sing, being, swimming")
    >>> word_filter(t, "*ing")
    [('sing', 2), ('swimming', 1), ('being', 1)]
    >>> word_filter(t, "??*ing")
    [('swimming', 1), ('being', 1)]
    """
    output = set()

    def helper(pattern, sofar, current_node):
        # base case
        if not pattern:
            if trie.getvalue(sofar) != None:
                output.add((sofar, trie[sofar]))
            return
        
        if not current_node.children:
            if all([c == '*' for c in pattern]):
                output.add((sofar, trie[sofar]))
            return
        
        cur = pattern[0]
        rest = pattern[1:]
        
        # recursive 
        if cur == "?":
            for child, child_node in current_node.children.items():
                helper(rest, sofar+child, child_node)

        elif cur == "*":
            # match 0 
            helper(rest, sofar, current_node)
            # match 1 or more 
            for child, child_node in current_node.children.items():
                helper(pattern, sofar+child, child_node)
            
        else:
            if cur in current_node.children:
                helper(rest, sofar+cur, current_node.children[cur])
            else:
                return

    helper(pattern, '', trie)

    return sorted(output)



# you can include test cases of your own in the block below.
if __name__ == '__main__':
    # doctest.testmod()
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)

    # t = make_word_trie("man mat mattress map me met a man a a a map man met")
    # result = word_filter(t, "**") 
    # print(result)



    # section 7 
    with open("Alice’s_Adventures_in_Wonderland.txt", encoding="utf-8") as f:
        Alice_in_Wonderland = f.read()

    with open("A_Tale_of_Two_Cities.txt", encoding="utf-8") as f:
        Two_Cities = f.read()

    with open("Pride_and_Prejudice.txt", encoding="utf-8") as f:
        Pride_and_Prejudice = f.read()
    
    with open("Dracula.txt", encoding="utf-8") as f:
        Dracula = f.read()
    
    with open("Metamorphosis.txt", encoding="utf-8") as f:
        Metamorphosis = f.read()

    # √ In Alice's Adventures in Wonderland, what are the six most common sentences (regardless of prefix)?
    # t = make_phrase_trie(Alice_in_Wonderland)
    # top6 = autocomplete(t, tuple(), 6)
    # print(top6)

    # √ In Metamorphosis, what are the six most common words starting with gre?
    # t = make_word_trie(Metamorphosis)
    # top6 = autocomplete(t, 'gre', 6)
    # print(top6)

    # In Metamorphosis, what are all of the words matching the pattern c*h, along with their counts?
    # t = make_word_trie(Metamorphosis)
    # res = word_filter(t, "c*h")
    # print(res)


    # In A Tale of Two Cities, what are all of the words matching the pattern r?c*t, along with their counts?
    # t = make_word_trie(Two_Cities)
    # res = word_filter(t, "r?c*t")
    # print(res)

    # √ What are the top 12 autocorrections for 'hear' in Alice in Wonderland?
    # t = make_word_trie(Alice_in_Wonderland)
    # top12 = autocorrect(t, 'hear', 12)
    # print(top12)

    # √ What are all autocorrections for 'hear' in Pride and Prejudice?
    # t = make_word_trie(Pride_and_Prejudice)
    # all = autocorrect(t, 'hear')
    # print(all)

    # √ How many distinct words are in Dracula?  
    # t = make_word_trie(Dracula)
    # distinct = only_keys(list(t))
    # print(len(distinct))

    # √ How many total words are in Dracula?
    # def total_word(text):
    #     counter = 0
    #     sentences = tokenize_sentences(text)
    #     for s in sentences:
    #         words = s.split(' ') # list of words in a sentence 
    #         for w in words:
    #             counter += 1
    #     return counter
    # total = total_word(Dracula)
    # print(total)

    # √ How many distinct sentences are in Alice's Adventures in Wonderland?
    # t = make_phrase_trie(Alice_in_Wonderland)
    # distinct = only_keys(list(t))
    # print(len(distinct))

    # √ How many total sentences are in Alice's Adventures in Wonderland?
    # def total_sentences(text):
    #     counter = 0
    #     sentences = tokenize_sentences(text)
    #     for s in sentences:
    #         counter += 1
    #     return counter
    # total = total_sentences(Alice_in_Wonderland)
    # print(total)