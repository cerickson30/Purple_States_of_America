import pandas as pd
import geopandas as gpd
import requests



def get_county_shapes(filename='US_counties_finer_boundaries.shp'):
    path = 'data/shape_files/US_counties_finer_boundaries/'
    county_shapes_gdf = gpd.read_file(path + f'{filename}')

    county_shapes_gdf = county_shapes_gdf.rename(columns={'name': 'County', 'state': 'State'})
    
    return county_shapes_gdf



def get_election_results(all_elections, district_gdf, year=2012):
    """INPUT: election_results: Dataframe of presidential election results, reported at the county level,
        year: year of presidential election
    OUTPUT: Map of county-level results, colored using RGB where Red level is based on percent of votes for
        the Republican candidate, Green level is based on the percent of votes for other candidate(s),
        and Blue level is based on percent of votes for the Democratic candidate.
    """
    
    year_results = all_elections.loc[all_elections.Year == year].reset_index(drop=True)

    year_results_gdf = district_gdf.merge(year_results, on=['State','County'], how='left')
    year_results_gdf.dropna(inplace=True)
    year_results_gdf['Year'] = year_results_gdf['Year'].astype(int)
    
    return year_results_gdf




def add_title_legend(mymap, year, dem_name, repub_name, other_name):
    from branca.element import Template, MacroElement

    str1 = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>The Purple States of America</title>
      <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

      <script>
      $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

      </script>
    </head>"""


    str2 = f"""<body>


    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:0px; background-color:rgba(255, 255, 255, 0.5);
         border-radius:0px; padding: 10px; font-size:34px; left: 0px; top: 0px;'>

    <div class='legend-title'>The Purple States of America {year}</div>
    </div>


    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:20px; right: 20px; top: 20px;'>

    <div class='legend-title'>Vote Share</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:#0000FF;opacity:1;'></span>{dem_name}</li>
        <li><span style='background:#FF0000;opacity:1;'></span>{repub_name}</li>
        <li><span style='background:#00FF00;opacity:1;'></span>{other_name}</li>
      </ul>
    </div>
    </div>

    </body>"""

    str3 = """</html>

    <style type='text/css'>
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 0px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 0px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""


    template = '\n'.join([str1, str2, str3])

    macro = MacroElement()
    macro._template = Template(template)

    mymap.get_root().add_child(macro)
    
    return mymap





def map_purple_states(all_elections, year=2012):
    """INPUT: all_elections - dataframe of election results
    year - A year of a presidential election, from 1960 through 2012
    OUTPUT: A map"""

    # import os, requests
    import folium
    from branca.element import Template, MacroElement
    
    if year < 1788 or year % 4 != 2020 % 4:
        print('Sorry, there was no presidential election in {}'.format(year))
        return None
    if year not in all_elections.Year.unique():
        print('Sorry, the election results data for {} are not accessible'.format(year))
        return None
    
    counties_gdf = get_county_shapes()
    
    election_results_gdf = get_election_results(all_elections, counties_gdf, year)
    
    mymap = folium.Map([38, -96], tiles='cartodbpositron', zoom_start=5)

    districts = folium.GeoJson(
        election_results_gdf,
        style_function = lambda feature: {
            'fillColor': feature['properties']['hex_color'],
            'fillOpacity':1 ,
            'color': 'grey',
            'weight': 1,
            'dashArray': '2, 5',
        }
    )

    districts.add_child(
        folium.features.GeoJsonTooltip(fields = ['State', 'County','Democrat', 'Republican', 'Other'], 
                                       aliases = ['State:', 'County:',
                                                  election_results_gdf['dem_name'][0]+':', 
                                                  election_results_gdf['repub_name'][0]+':',
                                                  election_results_gdf['other_name'][0]+':'])
    )

    districts.add_to(mymap)
    
    return mymap







