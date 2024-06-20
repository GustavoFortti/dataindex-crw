def get_url(conf, url):
    if (not conf["index"]):
        conf["index"] = 1
        return url #+ str(1)
    conf["index"] += 1
    return url + str(conf["index"])