import streamlit as st

from PIL import Image
import numpy as np

import optcbx

"""
# OPTC Box Exporter [PoC]

This web application aims to showcase the OPTC Box Exporter (OPTCbx) project.

OPTCbx is able to analyze your character box screenshot, and obtain all the 
characters within it, without any manual intervention.

By its own, OPTCbx, does not have any utility apart from showing your character 
box in a fancy manner. Power comes with the contributions. I believe that
OPTCbx can be a key point combined with projects such:

- [NakamaNetwork](https://www.nakama.network/): With OPTCbx you are not far from automatically exporting 
your teams to this amazing website.

- [CrewPlanner](https://www.reddit.com/r/OnePieceTC/comments/j60ueg/crew_planner_is_now_available/): Image that you can export all your characters to CrewPlanner
without spending hours introducing your character one by one. With OPTCbx, you
will be able to do so with just few minuts or even seconds 😲.

- [TM Planner](https://lukforce.bitbucket.io/tm-planner/): OPTCbx would provide the ability to automatically select the 
characters that you don't own.

## Try it out
"""

"""
Pick an image size. Larger image sizes enhance the results, but increases the
computation time.

> Sizes larger than 100 are not recommended due its high computational cost
"""

im_size = st.slider("Image size", min_value=32, max_value=128, value=64, step=2, 
                    format="%d")

im = st.file_uploader("Select a character box screenshot")
if im is not None:
    with st.spinner(text='Analyzing your character box... This may take a while'):
        im = np.array(Image.open(im))[..., ::-1]

        characters, thumbnails = optcbx.find_characters_from_screenshot(
            im, return_thumbnails=True, image_size=im_size)
        thumbnails = thumbnails[...,::-1]

    st.success(f"Found {len(characters)} characters in your box")
   
    for c, t in zip(characters, thumbnails):
        with st.beta_container():
            im_col, text_col = st.beta_columns([1, 5])
            im_col.image(t, use_column_width=True)
            text_col.text(c.name)

