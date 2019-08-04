"""
Defines how every single scrapping is performed and how the result is stored
"""

import json
import os
from PIL import Image
from io import BytesIO


def scrap(page, query, results_count, path):
    urls_and_thumbs = page.scrap_image_urls_and_thumbs(query, results_count, {'icolor': 'white'})

    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'info.json'), 'w') as out:
        json.dump({
            'urls': [url for url, _ in urls_and_thumbs],
            'query': query
        }, out, indent=2, sort_keys=True, ensure_ascii=False)

    for i, (url, thumb) in enumerate(urls_and_thumbs):
        Image.open(BytesIO(thumb)).save(os.path.join(path, f'{i}.thumb.png'), 'PNG')
