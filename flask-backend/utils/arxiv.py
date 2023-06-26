import re
import os
import arxiv
import tqdm
from pdfrw import PdfReader, PdfWriter
from pdfrw.findobjs import trivial_xobjs, wrap_object, find_objects
from pdfrw.objects import PdfDict, PdfArray, PdfName
import fitz

os.makedirs(f".pdf", exist_ok=True)
os.makedirs(f".images", exist_ok=True)


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

def download_paper_pdf(arxiv_id):
    paper = next(arxiv.Search(id_list=[arxiv_id]).results())

    if os.path.exists(f".pdf/{arxiv_id}.pdf"):
        return f".pdf/{arxiv_id}.pdf"

    pdf_file_path = paper.download_pdf(dirpath=f"./.pdf", filename=f"{arxiv_id}.pdf")
    return pdf_file_path

def download_paper_image(pdf_file_path, img_num=1):
    img_path = f".images/{pdf_file_path.split('/')[-1].replace('.pdf', '')}"
    os.makedirs(img_path, exist_ok=True)
    
    WIDTH = 8.5 * 72
    MARGIN = 0.5*72

    pdf = PdfReader(pdf_file_path)
    objects = []
    for xobj in list(find_objects(pdf.pages)):
        if xobj.Type==PdfName.XObject and xobj.Subtype == PdfName.Form:
            wrapped = wrap_object(xobj, WIDTH, MARGIN)
            objects.append(wrapped)
            if len(objects) >= img_num:
                break

    if not objects:
        raise IndexError("No XObjects found")
    writer = PdfWriter(img_path+"/tmp.pdf")
    writer.addpages(objects)
    writer.write()

    doc = fitz.open(img_path+"/tmp.pdf")
    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap()
        img_name = os.path.join(img_path, f'image{page_num+1}.png')
        pix.save(img_name)
    
    os.remove(img_path+"/tmp.pdf")

    return img_path