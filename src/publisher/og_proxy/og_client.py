from bs4 import BeautifulSoup, ResultSet
from requests import get

user_agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track
}

# Define common prefixes for social meta tags.
# This includes OpenGraph (og:), Twitter Cards (twitter:), Facebook (fb:),
# and specific OpenGraph object type properties (article:, profile:, book:).
social_prefixes = ('og:', 'twitter:', 'fb:', 'article:', 'profile:', 'book:')

def fetch_og_data(url: str) -> dict:

    def is_og_data_tag(tag: ResultSet) -> bool:
        if tag.has_attr("property") or tag.has_attr("name"):
            att = tag.get("property") if tag.has_attr("property") else tag.get("name")
            return len([prefix for prefix in social_prefixes if att.startswith(prefix)]) > 0
        return False

    def get_og_data_value(tag: ResultSet) -> tuple[str, str]:
        att = tag.get("property") if tag.has_attr("property") else tag.get("name")
        return att, tag.get("content")

    def as_dict(items: list[tuple[str, str]]) -> dict:
        return {k: v for k, v in items}

    def full_url(domain: str, path: str) -> str:
        if domain not in path:
            return f"https://{domain}{path}"
        return path

    r = get(url)
    r.raise_for_status()
    domain = url.split("/")[2]
    html = BeautifulSoup(r.content, 'html.parser')
    meta_tags = html.findAll("meta")
    raw_og_data = as_dict([get_og_data_value(tag) for tag in meta_tags if is_og_data_tag(tag)])
    link_tags = html.findAll("link")
    icon_urls = as_dict([(tag.get("rel")[0], full_url(domain, tag.get("href"))) for tag in link_tags if tag.get("rel") and "icon" in tag.get("rel")])
    return {
        "url": url,
        "remote_response_code": r.status_code,
        "domain": domain,
        "title": raw_og_data["og:title"] if "og:title" in raw_og_data else raw_og_data["twitter:title"],
        "description": raw_og_data["og:description"] if "og:description" in raw_og_data else raw_og_data["twitter:description"],
        "image": raw_og_data["og:image"] if "og:image" in raw_og_data else raw_og_data["twitter:image"],
        "icon": icon_urls["shortcut"] if "shortcut" in icon_urls else icon_urls["icon"],
        "raw": {
            "og_data": raw_og_data,
            "icons": icon_urls
        }
    }
