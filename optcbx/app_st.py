import streamlit as st

import functools

from PIL import Image
import numpy as np

import optcbx

class StopExecution(Exception):
    """Special Exception which does not display any output to the Streamlit app."""
    pass

def cache_on_button_press(label, **cache_kwargs):
    """Function decorator to memoize function executions.

    Parameters
    ----------
    label : str
        The label for the button to display prior to running the cached funnction.
    cache_kwargs : Dict[Any, Any]
        Additional parameters (such as show_spinner) to pass into the underlying @st.cache decorator.
    Example
    -------
    This show how you could write a username/password tester:
    >>> @cache_on_button_press('Authenticate')
    ... def authenticate(username, password):
    ...     return username == "buddha" and password == "s4msara"
    ...
    ... username = st.text_input('username')
    ... password = st.text_input('password')
    ...
    ... if authenticate(username, password):
    ...     st.success('Logged in.')
    ... else:
    ...     st.error('Incorrect username or password')
    """
    internal_cache_kwargs = dict(cache_kwargs)
    internal_cache_kwargs['allow_output_mutation'] = True
    internal_cache_kwargs['show_spinner'] = False
    
    def function_decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            @st.cache(**internal_cache_kwargs)
            def get_cache_entry(func, args, kwargs):
                class ButtonCacheEntry:
                    def __init__(self):
                        self.evaluated = False
                        self.return_value = None
                    def evaluate(self):
                        self.evaluated = True
                        self.return_value = func(*args, **kwargs)
                return ButtonCacheEntry()
            cache_entry = get_cache_entry(func, args, kwargs)
            if not cache_entry.evaluated:
                if st.button(label):
                    with st.spinner(text='Analyzing your character box... This may take a while'):
                        cache_entry.evaluate()
                else:
                    raise StopExecution
            return cache_entry.return_value
        return wrapped_func
    return function_decorator


@cache_on_button_press('Run export')
def process_image(im):
    if im is None:
        return [], []

    im = np.array(Image.open(im))[..., ::-1]

    characters, thumbnails = optcbx.find_characters_from_screenshot(
        im, 
        return_thumbnails=True, 
        dist_method=dist_method.lower(),
        image_size=im_size)
    thumbnails = thumbnails[...,::-1]
    return characters, thumbnails


def send_feedback(feedbacks):
    pass


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

"""
Method to find the closest character. SSIM gives better results but it is slower
than MSE.
"""
dist_method = st.radio("Distance method", ('SSIM', 'MSE'), index=1)
im = st.file_uploader("Select a character box screenshot")
optc_db_url = "https://optc-db.github.io/characters/#/view"

try:
    characters, thumbnails = process_image(im)
    st.success(f"Found {len(characters)} characters in your box")
    feedbacks = [''] * len(characters)
    for i, (c, t) in enumerate(zip(characters, thumbnails)):
        with st.beta_container():
            im_col, text_col, fb_col = st.beta_columns([1, 4, 1])

            im_col.image(t, use_column_width=False)
            text_col.markdown(f"[{c.name}]({optc_db_url}/{c.number})")

            feedbacks[i] = fb_col.radio('',
                                        ('Nice!', 'Bad :('),
                                        key=f'{i}_fb_radio')

    if st.button('Send feedback'):
        st.success("Thanks for your feedback. We appreciate it :)")
except StopExecution:
    pass