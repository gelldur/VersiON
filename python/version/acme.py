
def get_list(text):
    split_list = [x.strip()
                  for x in text.split(',')]
    split_list = list(filter(None, split_list))
    return split_list


def contains(find_list, text):
    for element in find_list:
        if element in text:
            return True
    return False
