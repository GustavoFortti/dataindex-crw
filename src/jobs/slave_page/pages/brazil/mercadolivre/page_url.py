def get_url(conf, seed):
    url = seed["url"]
    
    conf["index"] = 2
    if (not conf["index"]):
        conf["index"] = 1
        return url
    
    url = f"{url}{seed["next_url_tail"]}"
    
    if (conf["index"] == 1):
        conf["index"] += 1
        return url
    
    mercado_livre_indices = [None, "49", "97", "145", "193", "241", "289", "337", "385", "443", "481", "529", "577", "625"]
    last_index = mercado_livre_indices[conf["index"] - 1]
    index = mercado_livre_indices[conf["index"]]
    
    url = url.replace(last_index, index)
    return url