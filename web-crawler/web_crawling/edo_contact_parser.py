import re

from bs4 import BeautifulSoup
from web_crawling.web_crawler_errors import NoResultsFoundError


class EDOContactInfoParser:
    TAGS = ["Website URL", "Phone"]

    def __init__(self):
        pass

    def parse_contact_info(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        general_info_div = soup.find('div', text=re.compile("General Information", re.IGNORECASE))
        try:
            general_info_div = general_info_div.parent
        except AttributeError:
            raise NoResultsFoundError("Couldn't parse cause_iq results")
        dl_tags = general_info_div.find_all('dl')
        dl_dict = {}

        for dl in dl_tags:
            current_dt = None
            for child in dl.children:
                if child.name == 'dt' and child.get_text(strip=True) in self.TAGS:
                    current_dt = child.get_text(strip=True)
                    dl_dict[current_dt] = []
                elif child.name == 'dd' and current_dt:
                    if current_dt == "Website URL":
                        a_tag = child.find('a', href=True)
                        if a_tag:
                            dl_dict[current_dt].append(a_tag['href'])
                    elif current_dt == "Phone":
                        a_tag = child.find('a', href=True)
                        if a_tag:
                            dl_dict[current_dt].append(a_tag.get_text(strip=True))
                            break
                    else:
                        dl_dict[current_dt].append(child.get_text(strip=True))

        # Concatenate <dd> values
        for key in dl_dict:
            dl_dict[key] = ' '.join(dl_dict[key])

        return dl_dict
