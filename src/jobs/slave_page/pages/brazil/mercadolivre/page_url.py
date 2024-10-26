def get_url(conf, seed):
    url = seed["url"]
    
    if (not conf["index"]):
        conf["index"] = 1
        return url
    
    if (seed["remove_to_next_index"]):
        url = url.replace(seed["remove_to_next_index"], "")
    url = f"{url}{seed["next_url_tail"]}"
    
    if (conf["index"] == 1):
        conf["index"] += 1
        return url
    
    mercado_livre_indices = [None, "49", "97", "145", "193", "241", "289", "337", "385", "443", "481", "529", "577", "625"]
    last_index = mercado_livre_indices[conf["index"] - 1]
    index = mercado_livre_indices[conf["index"]]
    
    url = url.replace(last_index, index)
    return url