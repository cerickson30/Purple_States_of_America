import pandas as pd
import geopandas as gpd
import requests




def get_county_shapes(filename='US_counties_finer_boundaries.shp'):
    # github_url = 'https://raw.githubusercontent.com/cerickson30/Purple_States_of_America/main/'
    path = '../data/shape_files/US_counties_finer_boundaries/'
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


def map_purple_states(all_elections, year=2012):
    """INPUT: all_elections - dataframe of election results
    year - A year of a presidential election, from 1960 through 2012
    OUTPUT: A map"""

    import os, requests
    import folium
    
    
    # Check to see if the format_folium_map.py file exists, otherwise download it
    if not os.path.exists('format_folium_map.py'):
        # Get the file from Dr. Erickson's github repo
        url = 'https://raw.githubusercontent.com/cerickson30/Purple_States_of_America/main/code/format_folium_map.py'
        r = requests.get(url, allow_redirects=True)

        # Save the contents to 'format_folium_map.py', note that the contents 
        # are returned in byte form so we need to use mode='wb'
        outfile = open('format_folium_map.py', mode='wb')
        outfile.write(r.content)
        outfile.close() # remember to close the connection to the file
        
    
    from format_folium_map import add_title_legend
    
    if year < 1788 or year % 4 != 2020 % 4:
        print('Sorry, there was no presidential election in {}'.format(year))
        return None
    if year not in all_elections.Year.unique():
        print('Sorry, the election results data for {} are not accessible'.format(year))
        return None
    
    counties_gdf = get_county_shapes()
    
    election_results_gdf = get_election_results(all_elections, counties_gdf, year)
    
    mymap = folium.Map([38, -100], tiles='cartodbpositron', zoom_start=5)

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
    
    mymap = add_title_legend(mymap, year = year, dem_name=election_results_gdf['dem_name'][0],
                             repub_name = election_results_gdf['repub_name'][0], 
                             other_name = election_results_gdf['other_name'][0])

    return mymap