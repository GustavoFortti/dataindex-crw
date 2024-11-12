def get_url(conf, seed):
    url = seed["url"]
    if (not conf["index"]):
        conf["index"] = 1
        return url + str(conf["index"])
    conf["index"] += 1
    return url + str(conf["index"])