from enum import Enum

from lxml import etree


class TorrentSite(Enum):
    NYAA = "https://nyaa.si"
    SUKEBEI = "https://sukebei.nyaa.si"


def parse_site(request_text: str, site: TorrentSite, **params) -> dict:
    parser = etree.HTMLParser()
    tree = etree.fromstring(request_text, parser)
    uri = site.value

    website = {}
    torrents = []

    for tr in tree.xpath("//tbody//tr"):
        block = []

        for td in tr.xpath("./td"):
            for link in td.xpath("./a"):

                href = link.attrib.get("href").split('/')[-1]

                if href[-9:] != "#comments":
                    block.append(href)

                    if link.text and link.text.strip():
                        block.append(link.text.strip())

            if td.text is not None and td.text.strip():
                block.append(td.text.strip())

        # Add type of torrent based on tr class.
        if tr.attrib.get("class") is not None:
            if 'danger' in tr.attrib.get("class"):
                block.append("remake")
            elif 'success' in tr.attrib.get("class"):
                block.append("trusted")
            else:
                block.append("default")
        else:
            block.append("default")

        _category = ''.join(tr.xpath(
            "./td[1]/a[1]/img[@class='category-icon'][1]/@alt"
        ))
        try:
            torrents.append({
                'id': block[1],
                'category': _category,
                'url': f"{uri}/view/{block[1]}",
                'name': block[2],
                'download_url': f"{uri}/download/{block[3]}",
                'magnet': block[4],
                'size': block[5],
                'date': block[6],
                'seeders': block[7],
                'leechers': block[8],
                'completed_downloads': block[9],
                'type': block[10]
            })
        except IndexError:
            pass

    last_page = tree.xpath("//ul[@class='pagination']//li//a/text()")
    input_query = ''.join(tree.xpath(
        "//input[@class='form-control'][1]/@value"
    ))

    if input_query == "":
        total_page = 100
    else:
        try:
            total_page = int(last_page[-2])
        except IndexError:
            total_page = 1

    website["total_page"] = total_page
    website["keyword"] = params["q"]
    website["category"] = params["c"].split('_')[0]
    website["subcategory"] = params["c"].split('_')[1]
    website["page"] = params["p"]
    website["filters"] = params["f"]
    website["sort"] = params["s"]
    website["order"] = params["o"]
    website["torrents"] = torrents

    return website


def parse_single(request_text: str, site: TorrentSite) -> dict:
    parser = etree.HTMLParser()
    tree = etree.fromstring(request_text, parser)
    uri = site.value

    torrent = {}
    meta = []
    comments = []

    for row in tree.xpath("//div[@class='row']"):
        for div_text in row.xpath("./div[@class='col-md-5']//text()"):
            if div_text.strip():
                meta.append(div_text.strip())

    torrent['title'] = tree.xpath(
        "//h3[@class='panel-title']/text()"
    )[0].strip()
    torrent['category'] = f"{meta[0]} - {meta[2]}"
    torrent['uploader'] = meta[4]
    torrent['uploader_profile'] = ''.join(str(f"{uri}/user/{meta[4]}"))
    torrent['website'] = meta[6]
    torrent['size'] = meta[8]
    torrent['date'] = meta[3]
    torrent['seeders'] = meta[5]
    torrent['leechers'] = meta[7]
    torrent['completed'] = meta[9]
    torrent['hash'] = meta[10]
    magnet_uri = tree.xpath("//a[@class='card-footer-item'][1]//@href")
    torrent['magnet'] = ''.join(magnet_uri)
    torrent["comments"] = comments

    torrent['description'] = ""

    for s in tree.xpath("//div[@id='torrent-description']"):
        torrent['description'] += s.text

    cmt_text = tree.xpath("//div[@class='comment-content']/text()")
    cmt_author = tree.xpath("//div[@class='col-md-2'][1]/p[1]/a/text()[1]")
    cmt_img = tree.xpath("//img[@class='avatar'][1]/@src")
    cmt_time = tree.xpath(
        "//div[@class='row comment-details'][1]/a[1]/small[1]/text()[1]"
    )
    for author, time, text, img in zip(cmt_author, cmt_time, cmt_text, cmt_img):
        comments.append({
            "author": author,
            "time": time,
            "text": text,
            "image": img
        })

    _files_list_path = "//div[@class='torrent-file-list panel-body'][1]//li"

    files_list = list(tree.xpath(f"{_files_list_path}/text()"))
    stripped_files_list = (list(map(lambda file: file.strip(), files_list)))
    filtered_file_list = list(filter(None, stripped_files_list))
    files_sizes = list(tree.xpath(
        f"{_files_list_path}//span[@class='file-size']/text()")
    )
    stripped_sizes_list = (list(map(lambda sizes: sizes.strip(), files_sizes)))

    mixed = dict(zip(filtered_file_list, stripped_sizes_list))

    files = []
    for key in mixed:
        files.append({
            "file": key,
            "size": mixed[key][1:-1]
        })

    torrent['files_list'] = files

    return torrent
