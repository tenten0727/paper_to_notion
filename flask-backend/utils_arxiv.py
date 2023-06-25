import re
import arxiv

def get_paper_info(url):
    # Extract the ID from the URL
    id_pattern = r'(\d+\.\d+)'
    id_match = re.search(id_pattern, url)
    if id_match is not None:
        paper_id = id_match.group(1)
        # Use the arxiv library to get the paper info
        search = arxiv.Search(id_list=[paper_id])
        paper = next(search.results())
        return {
            "id": paper_id,
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "published": paper.published,
            "updated": paper.updated,
            "pdf_url": paper.pdf_url,
        }
    else:
        return None
