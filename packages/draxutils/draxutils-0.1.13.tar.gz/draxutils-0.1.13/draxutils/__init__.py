
# myutils/__init__.py

import pandas as pd
from io import BytesIO
import base64
from PIL import Image
from typing import List, Union
from .timer import *
from .html_util import *

def get_thumbnail(path):
    """
    Generate a thumbnail of an image.

    Parameters:
    path (str): The file path to the image.

    Returns:
    PIL.Image: The thumbnail image.
    """
    i = Image.open(path)
    i.thumbnail((150, 150), Image.LANCZOS)
    return i

def image_base64(im):
    """
    Convert an image to a base64 string.

    Parameters:
    im (str or PIL.Image): The image or the path to the image.

    Returns:
    str: Base64 encoded string of the image.
    """
    if isinstance(im, str):
        im = get_thumbnail(im)
    with BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    """
    Format an image for HTML display.

    Parameters:
    im (str or PIL.Image): The image or the path to the image.

    Returns:
    str: HTML string for displaying the image.
    """
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'

def imglist_formatter(imglist):
    """
    Format a list of images for HTML display.

    Parameters:
    imglist (list): List of images or paths to images.

    Returns:
    str: HTML string for displaying the images.
    """
    if imglist[0] is None:
        return ""
    return " ".join([f'<img src="data:image/jpeg;base64,{image_base64(im)}">' for im in imglist])

import pandas as pd
from io import BytesIO
import base64
from PIL import Image
from typing import List, Union, Dict
from IPython.display import display, HTML

def show_pd(df, image_key: Union[str, List[str]]='image', imagelist_key: Union[str, List[str]]='masks',
            column_widths: Union[List[str], str, Dict[str, str]] = None,
            column_alignments: Union[List[str], str, Dict[str, str]] = None):
    """
    Display a pandas DataFrame with formatted image columns in Jupyter Notebook,
    with flexible control over column widths and alignments.

    Parameters:
    df (pandas.DataFrame): The DataFrame to display.
    image_key (str or List[str]): The key(s) of the column(s) containing the image. Can be path or list of paths.
    imagelist_key (str or List[str]): The key(s) of the column(s) containing the list of images. Can be path or list of paths.
    column_widths (List[str], str, or Dict[str, str]):
        - If List[str]: width specifications for columns, in order from left to right (e.g., ['30%', '100px']).
        - If str: a single width to be applied to all columns (e.g., '100px').
        - If Dict[str, str]: a dictionary mapping column names to their widths (e.g., {'col1': '30%', 'col2': '100px'}).
        - If None: columns will have even widths.
    column_alignments (List[str], str, or Dict[str, str]):
        - If List[str]: alignment specifications for columns, in order from left to right (e.g., ['left', 'center']).
        - If str: a single alignment to be applied to all columns (e.g., 'center').
        - If Dict[str, str]: a dictionary mapping column names to their alignments (e.g., {'col1': 'left', 'col2': 'center'}).
        - If None: no specific alignment is applied.

    Returns:
    IPython.core.display.HTML: The HTML representation of the DataFrame.
    """
    if isinstance(image_key, str):
        image_key = [image_key]
    if isinstance(imagelist_key, str):
        imagelist_key = [imagelist_key]

    formatters = {
        **{img_key: image_formatter for img_key in image_key},
        **{imglist_key: imglist_formatter for imglist_key in imagelist_key}
    }

    html = df.to_html(formatters=formatters, escape=False, index=False)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    headers = soup.find_all('th')
    column_names = [header.text for header in headers]

    # Process column_widths based on input type
    if isinstance(column_widths, str):
        column_widths = [column_widths] * len(headers)
    elif isinstance(column_widths, dict):
        column_widths = [column_widths.get(name, None) for name in column_names]
    elif column_widths is None:
        even_width = f"{100 / len(headers):.2f}%"
        column_widths = [even_width] * len(headers)

    # Process column_alignments based on input type
    if isinstance(column_alignments, str):
        column_alignments = [column_alignments] * len(headers)
    elif isinstance(column_alignments, dict):
        column_alignments = [column_alignments.get(name, None) for name in column_names]

    # Ensure column_widths and column_alignments match the number of columns
    column_widths = (column_widths + [None] * len(headers))[:len(headers)]
    if column_alignments:
        column_alignments = (column_alignments + [None] * len(headers))[:len(headers)]

    for i, header in enumerate(headers):
        style = ""
        if column_widths[i]:
            style += f"width: {column_widths[i]};"
        if column_alignments and column_alignments[i]:
            style += f" text-align: {column_alignments[i]};"
        if style:
            header['style'] = style

        # Apply alignment to all cells in the column
        if column_alignments and column_alignments[i]:
            for row in soup.find_all('tr')[1:]:  # Skip header row
                cell = row.find_all('td')[i]
                cell['style'] = cell.get('style', '') + f" text-align: {column_alignments[i]};"

    return HTML(str(soup))

# def show_pd(df, image_key: Union[str, List[str]]='image', imagelist_key: Union[str, List[str]]='masks'):
#     """
#     Display a pandas DataFrame with formatted image columns in Jupyter Notebook.

#     Parameters:
#     df (pandas.DataFrame): The DataFrame to display.
#     image_key (str): The key of the column containing the image. Can be path or list of paths.
#     imagelist_key (str): The key of the column containing the list of images. Can be path or list of paths.

#     Returns:
#     IPython.core.display.HTML: The HTML representation of the DataFrame.
#     """
#     from IPython.display import display, HTML
#     if isinstance(image_key, str):
#         image_key = [image_key]
#     if isinstance(imagelist_key, str):
#         imagelist_key = [imagelist_key]
#     return HTML(df.to_html(formatters={**{img_key: image_formatter for img_key in image_key},
#                                         **{imglist_key: imglist_formatter for imglist_key in imagelist_key}},
#                            escape=False))
