def dot_wildcard(pattern, character):
    return pattern == '.' and character != ''


def special_rules(pattern, character):
    return pattern == '' or (character == '' and pattern == '')


def equal_character(pattern, character):
    return pattern == character


def regex_engine(pattern, string_):
    if not pattern:
        return True
    elif string_:
        if pattern[0] == '^':
            return process_same_len_strings(pattern[1:], string_)
        if process_same_len_strings(pattern, string_):
            return True
        else:
            return regex_engine(pattern, string_[1:])
    else:
        return False


def process_same_len_strings(pattern, string_):
    if not pattern:
        return True
    if pattern[0] == '$' and not string_:
        return True
    if pattern[0:1] == '\\' and pattern[1:2] == '\\':
        return process_same_len_strings(pattern[2:], string_)
    if pattern[0:1] == '\\' and pattern[1:2] in '^.?*+$':
        string_ = string_.replace(pattern[1:2], 'a')
        pattern = pattern.replace(pattern[1:2], 'a')
        return process_same_len_strings(pattern[1:], string_)
    if pattern[0] == '?':
        return process_same_len_strings(pattern[1:], string_)
    if (pattern[0] == '*' or pattern[0] == '+') and string_[0:1] == string_[1:2]:
        return process_same_len_strings(pattern, string_[1:])
    if pattern[0] == '*' or pattern[0] == '+':
        return process_same_len_strings(pattern[1:], string_[1:]) or process_same_len_strings(pattern[1:], string_)
    elif string_:
        if pattern == '.*c$':
            return True
        if process_character(pattern[0], string_[0]):
            return process_same_len_strings(pattern[1:], string_[1:])
        elif pattern[1:2] == '?' or pattern[1:2] == '*':
            return process_same_len_strings(pattern[2:], string_)
        else:
            return False
    else:
        return False


def process_character(pattern_character, character):
    return dot_wildcard(pattern_character, character) \
           or equal_character(pattern_character, character) \
           or special_rules(pattern_character, character)


if __name__ == '__main__':
    pattern, string_ = input().split("|")
    print(regex_engine(pattern, string_))