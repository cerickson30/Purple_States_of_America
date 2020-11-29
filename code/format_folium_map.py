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