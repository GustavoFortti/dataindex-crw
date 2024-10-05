def get_url(conf, url):
    if conf['index'] is None:
        conf['index'] = 1
        return url
    
    soup = conf['soup']
    
    next_page = soup.find('a', class_='andes-pagination__link', title='Seguinte')
    if next_page is None:
        conf['index'] = None
        return None
    
    next_page_url = next_page.get('href') if next_page else None
    if "" == next_page_url:
        conf['index'] = None
        return None
    
    conf['index'] += 1
    return next_page_url