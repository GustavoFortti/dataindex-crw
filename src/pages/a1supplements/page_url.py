def get_url(url: str, index: int, seed: object) -> str:
    """
    Gera uma URL incrementada com base no índice fornecido.

    Args:
        url (str): A base da URL.
        index (Optional[int]): O índice atual, ou None se ainda não inicializado.
        seed (object): Um objeto contendo o atributo `url`.

    Returns:
        str: A URL completa com o índice.
    """
    seed_url = seed["url"]

    if index is None:
        index = 1
        return f"{seed_url}{index}"

    index += 1
    return f"{seed_url}{index}"