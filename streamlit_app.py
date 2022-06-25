import pandas as pd
from app_mapping_functions import map_purple_states
import requests

# Streamlit and customization stuff
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

# For the custom footnote
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

st.set_page_config(
    page_title='The Purple States of America',
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
    )


# Get and preprocess data
@st.experimental_singleton
def load_data():
    return  pd.read_csv('data/all_years_with_colors.csv')


election_results = load_data()


years = ['Choose Year']
election_years = sorted(election_results['Year'].unique(), reverse=True)
years.extend([int(year) for year in election_years])


@st.experimental_singleton
class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=700)





# Streamlit stuff
with st.sidebar:
    year_choice = st.sidebar.selectbox('', years)



if type(year_choice) != int:
    st.title('The Purple States of America')

    col1, col2, col3 = st.columns([2,2,1.5])

    with col1:
        obama_purple_states_tweet = 'https://twitter.com/BarackObama/status/197162005830963201'
        tweet = Tweet(obama_purple_states_tweet).component()
    with col2:
        min_year = min(years[1:])
        max_year = max(years[1:])

        st.markdown("""
            <style>
            .big-purple {
                font-size:20px !important;
                color: purple;
            }
            </style>
            <style>
            .big-font {
                font-size:20px !important;
            }
            </style>
            """, unsafe_allow_html=True)

        welcome_message = f"""<p class="big-purple">Despite the maps you see on election night---and no matter in which state or county you live---you
         live in a community where some people voted for the same candidate as you and where some people voted for a different candidate.</p>
         <p class="big-font">Select an election year from the menu on the left to see an interactive map of county-level presidential election results for elections from {min_year} through {max_year}.</p>
         """
    
        st.markdown(welcome_message, unsafe_allow_html=True)


else:
    dem_candidate = election_results.loc[election_results.Year == year_choice].dem_name.iloc[0]
    repub_candidate = election_results.loc[election_results.Year == year_choice].repub_name.iloc[0]
    other_candidate = election_results.loc[election_results.Year == year_choice].other_name.iloc[0]

    st.title(f'The Purple States of America {year_choice}: {dem_candidate} vs. {repub_candidate} vs. {other_candidate}')
    m = map_purple_states(election_results, year_choice)
    # call to render Folium map in Streamlit with specified dimensions
    st_folium(m, width=1350, height=750)

    if year_choice <= 1980:
        st.markdown('Note: Prior to 1983, the area of La Paz County, Arizona was part of Yuma County. Prior to 1981, Cibola County, New Mexico was part of Valencia County.')


data_source_message = "County shape data and results for elections prior to 2016 originally sourced from [Nifty Projects Purple America](http://nifty.stanford.edu/2014/wayne-purple-america/). County results for 2016 and 2020 sourced from Wikipedia."
st.markdown(data_source_message)






# For the custom footer in Streamlit app
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="60px",
        opacity=0.7,
    )

    style_hr = styles(
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer(author_name="Craig Erickson", author_url="https://cerickson30.github.io"):
    myargs = [
        "Made with Python 3.9 ",
        link("https://www.python.org/", image('https://i.imgur.com/ml09ccU.png',
        	width=px(18), height=px(18), margin= "0em")),
        " and Streamlit ",
        link("https://streamlit.io/", image('https://docs.streamlit.io/logo.svg',
        	width=px(24), height=px(25), margin= "0em")),
        " by ",
        link(author_url, author_name, color="#ff0000"),
        br(),
    ]
    layout(*myargs)


footer()