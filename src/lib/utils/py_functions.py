def flatten_list(list_of_lists):
    if list_of_lists is None:
        return []

    flattened_list = []
    for element in list_of_lists:
        if isinstance(element, list):
            for subelement in element:
                flattened_list.append(subelement)
        else:
            flattened_list.append(element)
    return flattened_list