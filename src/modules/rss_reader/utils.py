from typing import Union


def verify_link(link: str) -> bool:
    return link.startswith('magnet') or link.endswith('.torrent')


def find_link(links) -> Union[str, None]:
    for link in links:
        if link['type'] == "application/x-bittorrent" \
                and verify_link(link['href']):
            return link['href']
