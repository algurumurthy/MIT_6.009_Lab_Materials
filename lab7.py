# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        self.value = None
        self.children = {}
        self.type = None


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if self.type is None:
            self.type = type(key)
        if type(key) != self.type:
            raise TypeError
        if len(key) == 0:
            self.value = value
        else:
            prefix = key[:1]
            suffix = key[1:]
            if prefix in self.children:
                self.children[prefix][suffix] = value
            else:
                im_trie = Trie()
                im_trie.type = self.type
                self.children[prefix] = im_trie
                self.children[prefix][suffix] = value


    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key) != self.type and self.type is not None:
            raise TypeError
        if len(key) == 0:
            if self.value is None:
                raise KeyError
            return self.value
        prefix = key[:1]
        suffix = key[1:]
        if prefix not in self.children.keys():
            raise KeyError
        else:
            return self.children[prefix][suffix]
        
        
    def find_subtrie(self, key):
        """
        Given a key, returns the entire "trie" structure associated with the key
        If the given key is not in the trie, raise a KeyError.  If the given key 
        is of the wrong type, raise a TypeError.
        """
        if type(key) != self.type and self.type is not None:
            raise TypeError
        if len(key) == 0:
            return self
        prefix = key[:1]
        suffix = key[1:]
        if prefix not in self.children.keys():
            raise KeyError
        else:
            return self.children[prefix].find_subtrie(suffix)
        

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key) != self.type:
            raise TypeError
        if self.type is None:
            self.type = type(key)
        if len(key) == 0:
            if self.value is None:
                raise KeyError
            self.value = None
        if self.__contains__(key):
            self.__setitem__(key, None)
        else:
            raise KeyError
        

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        try: 
            self.__getitem__(key)
            return True
        except KeyError:
            return False
        

    def help_iterate(self, suffix):
        if self.value is not None:
            yield (suffix, self.value)
        for key, value in self.children.items():
            yield from self.children[key].help_iterate(suffix + key)


    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        yield from self.help_iterate(self.type())


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    full_sentence = tokenize_sentences(text)
    trie = Trie()
    for sentence in full_sentence:
        sentence_list = sentence.split()
        for word in sentence_list:
            if word in trie:
                trie[word] += 1
            else:
                trie[word] = 1
    return trie


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    full_sentences = tokenize_sentences(text)
    trie = Trie()
    for sentence in full_sentences:
        phrase_list = sentence.split()
        final_tuple = tuple(phrase_list)
        if final_tuple in trie:
            trie[final_tuple] += 1
        else:
            trie[final_tuple] = 1
    return trie


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    if type(prefix) != trie.type:
        raise TypeError
    element_dict = {}
    try:
        sub_trie = trie.find_subtrie(prefix)
    except KeyError: 
        return []
    for key, value in sub_trie:
        element_dict[prefix+key] = value
    final_list = []
    if max_count is None:
        return list(element_dict.keys())
    else:
        new_dict = {k: v for k, v in sorted(element_dict.items(), key=lambda item: item[1])}
        key_list = list(new_dict.keys())
        key_list.reverse()
        if max_count > len(key_list):
            return key_list
        else:
            for i in range(max_count):
                final_list.append(key_list[i])
            return final_list


def transposition_helper(word_list, prefix):
    alphabet_set = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    im_list = word_list
    for index in range(len(prefix)):
        im_list.append(prefix[:index] + prefix[index+1:])
        im_list.append(prefix[:index]+ prefix[index+1:index+2] + prefix[index:index+1] + prefix[index+2:])
        for letter in alphabet_set:
            im_list.append(prefix[:index] + letter + prefix[index:])
            im_list.append(prefix[:index] + letter + prefix[index+1:])
    return im_list


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    word_list = autocomplete(trie, prefix, max_count)
    final_list = word_list.copy()
    if len(word_list) != max_count or max_count is None:
        input_words = word_list.copy()
        all_words = transposition_helper(input_words, prefix)
        verified_words = {}
        for word in all_words:
            if trie.__contains__(word):
                verified_words[word] = trie[word]
        if max_count is None:
            return list(set(word_list + list(verified_words.keys())))
        new_dict = {k: v for k, v in sorted(verified_words.items(), key=lambda item: item[1])}
        key_list = list(new_dict.keys())
        key_list.reverse()
        if max_count > len(key_list):
            return list(set(final_list + key_list))
        else:
            i = 0
            while i < len(key_list):
                if len(final_list) == max_count:
                    return final_list
                if key_list[i] not in final_list:
                    final_list.append(key_list[i])
                i += 1
    else:
        return autocomplete(trie, prefix, max_count)


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    if type(pattern) is not list:
        pattern = [pattern, '']
    tuple_list = []
    if trie.value is not None and pattern[0] == '':
        tuple_list.append((pattern[1], trie.value))
        return tuple_list
    if trie.value is None and pattern[0] == '':
        return []
    prefix = pattern[0][0]
    suffix = pattern[0][1:]
    if prefix == '*':
        new_pattern = [suffix, pattern[1]]
        tuple_list.extend(word_filter(trie, new_pattern))
    for key, value in trie.children.items():
        if prefix == '?':
            new_pattern = [suffix, pattern[1]+key]
            tuple_list.extend(word_filter(value, new_pattern))
        elif prefix == key:
            new_pattern = [suffix, pattern[1]+key]
            tuple_list.extend(word_filter(value, new_pattern))
        elif prefix == '*':
            new_pattern = [pattern[0], pattern[1]+key]
            tuple_list.extend(word_filter(value, new_pattern))
    return list(set(tuple_list))


# you can include test cases of your own in the block below.
if __name__ == '__main__':
#    alphabet_set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
#    with open("Wonderland.txt", encoding="utf-8") as f:
#        text = f.read()
#    length = 0
#    for letter in alphabet_set:
#        length += len(autocomplete(make_word_trie(text), letter, float('inf')))
#    print(length)
    pass
