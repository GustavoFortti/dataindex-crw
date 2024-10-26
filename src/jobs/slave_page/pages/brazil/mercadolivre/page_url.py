def get_url(conf, seed):
    url = seed["url"]
    
    if not conf.get("index"):
        conf["index"] = 1
        return url
    
    if conf["index"] == 1 and seed.get("next_url_tail") not in url:
        url = f"{url}{seed['next_url_tail']}"
    
    mercado_livre_indices = [None, "49", "97", "145", "193", "241", "289", "337", "385", "443", "481", "529", "577", "625"]
    
    if conf["index"] >= len(mercado_livre_indices):
        return url

    last_index = mercado_livre_indices[conf["index"] - 1]
    index = mercado_livre_indices[conf["index"]]

    if last_index:
        url = url.replace(last_index, index)
    
    seed["url"] = url
    conf["index"] += 1
    
    return url
