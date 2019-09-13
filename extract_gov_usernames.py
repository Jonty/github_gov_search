from collections import defaultdict
import json

import requests
from lxml import html
from slugify import slugify

req = requests.get("https://government.github.com/community/")
root = html.fromstring(req.content)

categories = defaultdict(lambda: defaultdict())

rows = root.xpath('//*[@class="org-include"]')
for row in rows:
    category_nodes = row.xpath("./h2")
    category = slugify(category_nodes[0].text_content())

    area_nodes = row.xpath('./*[@class="org-type clearfix"]')
    for area_node in area_nodes:
        area = area_node.xpath(".//h3")[0].text_content()
        area = slugify(" ".join(area.split(" ")[:-1]))

        org_nodes = area_node.xpath('.//*[@class="org-name text-small"]')
        orgs = [node.text_content().strip() for node in org_nodes]
        categories[category][area] = orgs

print(json.dumps(categories, indent=4))
