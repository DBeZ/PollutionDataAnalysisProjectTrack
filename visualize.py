import altair as alt
import altair_saver
import arabic_reshaper
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from bidi import algorithm as bidialg
import folium
import os
import geoviews as gv
import geoviews.tile_sources as gvts
from geoviews import dim, opts
from bokeh.models import HoverTool


###################
# Code for graphs #
###################

# Correct mirror string for string
def correct_heb_mirror_string(heb):
    reshaped_title = arabic_reshaper.reshape(heb)
    reshaped_title = bidialg.get_display(reshaped_title)
    return reshaped_title


# Correct mirror list of strings
def correct_heb_mirror_list(heb_list):
    corrected_list = []
    for title in heb_list:
        reshaped_title = correct_heb_mirror_string(title)
        corrected_list.append(reshaped_title)
    return corrected_list


# Maximize figure window to fullscreen
def make_fullscreen():
    bck = matplotlib.get_backend()
    if (bck == "Qt5Agg") or (bck == "Qt4Agg"):
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
    elif bck == "TkAgg":
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
    elif bck == "wxAgg":
        manager = plt.get_current_fig_manager()
        manager.frame.Maximize(True)

    plt.pause(0.001)  # without this delay fullscreen only takes hold if plt.show() is used


# Save matplotlib figure
def save_figure(figure_name):
    plt.savefig(fname=figure_name, bbox_inches='tight')
    plt.close()


# Bar plot comparing accidental and non accidental emissions
def accidents_with_non_acci(dataframes, col_by, col_of, title_template, col_name, is_x_rtl=False, is_log=False):
    for dataframe in dataframes:
        # Arrange data columns and legend
        title_heb = title_template.format(dataframe[col_of][0], dataframe["SugPlita"][0], col_name)
        title_heb_reversed = correct_heb_mirror_string(title_heb)
        data_series = ['KamutPlitaLoBeTeunot', 'KamutPlitaBeTeunot']
        new_legend = correct_heb_mirror_list(['כמות פליטה בשגרה', 'כמות פליטה בתאונות'])
        pv = pd.pivot_table(data=dataframe, values=data_series, index=[col_by], aggfunc="sum")
        pv.dropna(axis=0, how='any', inplace=True)
        pv = pv.loc[~(pv == 0).any(axis=1)]

        # pv.to_csv(title_heb+".txt", sep='\t', mode='a')

        # Plot
        if pv.size != 0:
            pv.plot.bar(log=is_log, stacked=False)
            ax = plt.gca()
            fig = plt.gcf()
            # Legend
            ax.legend(new_legend)
            # Figure title
            ax.set_title(title_heb_reversed, fontsize=16)
            # y axis label and ticks
            label_yaxis = "פליטה (Kg)"
            if is_log:
                label_yaxis = "פליטה (log Kg)"
            label_yaxis = correct_heb_mirror_string(label_yaxis)
            ax.set_ylabel(ylabel=label_yaxis)
            # x axis label and ticks
            label_xaxis = correct_heb_mirror_string(col_name)
            ax.set_xlabel(xlabel=label_xaxis)
            if is_x_rtl:
                correct_ticks_labels = correct_heb_mirror_list(pv.axes[0])
                ax = plt.gca()
                ax.set_xticklabels(labels=correct_ticks_labels)
            plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
                     rotation_mode="anchor", fontsize=6)
            fig.autofmt_xdate()

            plt.tight_layout()
            make_fullscreen()
            # plt.show(block=False)
            save_figure(figure_name=title_heb)


# Bar plot displaying accidental or non accidental emissions
def accidents_or_non_acci(dataframes, col_by, col_of, title_template, col_name, data_series, is_x_rtl=False,
                          is_log=False):
    for dataframe in dataframes:
        # Arrange data columns and legend
        title_heb = title_template.format(dataframe[col_of][0], dataframe["SugPlita"][0], col_name)
        title_heb_reversed = correct_heb_mirror_string(title_heb)
        pv = pd.pivot_table(data=dataframe, values=data_series, index=[col_by], aggfunc="sum")
        pv.dropna(axis=0, how='any', inplace=True)
        pv = pv.loc[~(pv == 0).any(axis=1)]

        # pv.to_csv(title_heb + ".txt", sep='\t', mode='a')

        # Plot
        if pv.size != 0:
            pv.plot.bar(log=is_log, stacked=False, legend=False)
            ax = plt.gca()
            fig = plt.gcf()
            # Legend
            # Figure title
            ax.set_title(title_heb_reversed, fontsize=16)
            # y axis label and ticks
            label_yaxis = "פליטה (Kg)"
            if is_log:
                label_yaxis = "פליטה (log Kg)"
            label_yaxis = correct_heb_mirror_string(label_yaxis)
            ax.set_ylabel(ylabel=label_yaxis)
            # x axis label and ticks
            label_xaxis = correct_heb_mirror_string(col_name)
            ax.set_xlabel(xlabel=label_xaxis)
            if is_x_rtl:
                correct_ticks_labels = correct_heb_mirror_list(pv.axes[0])
                ax = plt.gca()
                ax.set_xticklabels(labels=correct_ticks_labels)
            plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
                     rotation_mode="anchor", fontsize=6)
            fig.autofmt_xdate()

            plt.tight_layout()
            make_fullscreen()
            # plt.show(block=False)
            save_figure(figure_name=title_heb)


# Pie chart
def pie_plot(outer_data, outer_col, inner_data, inner_col, outer_label, inner_label, title_heb):
    # Outer Ring
    fig, ax = plt.subplots()
    ax.axis('equal')
    mypie, _ = ax.pie(outer_data[outer_col], radius=1.3, labels=outer_label)
    plt.setp(mypie, width=0.3, edgecolor='white')
    # Inner Ring
    mypie2, _ = ax.pie(inner_data[inner_col], radius=1.3 - 0.3, labels=inner_label, labeldistance=0.7)
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0, 0)
    plt.tight_layout()
    make_fullscreen()
    # plt.show(block=False)
    save_figure(figure_name=title_heb)


# Petal Scatter plot with color indicating category and size indicating value
def multi_feat_scatter(data, filename, x_col, y_col, size_col, color_col):
    chart = alt.Chart(data).mark_circle().encode(
        alt.X(x_col, scale=alt.Scale(zero=False)),
        alt.Y(y_col, scale=alt.Scale(zero=False, padding=1)),
        color=color_col,
        size=size_col
    )
    chart.configure_header(
        titleColor='Black',
        titleFontSize=30,
        labelColor='red',
        labelFontSize=14
    )

    altair_saver.save(chart, filename + ".html")


# Violin plot for multiple series - two series on one violin
def violin_emissions(data, x_col, y_col, hue, split, figure_name, fig_title, is_x_rtl=False):
    ax = sns.violinplot(x=x_col, y=y_col, hue=hue, split=split, data=data, palette="Set2")
    # y axis label and ticks
    # ax.set_yscale("log")
    # label_yaxis = "סך פליטה (log Kg)"
    label_yaxis = "סך פליטה (Kg)"
    label_yaxis = correct_heb_mirror_string(label_yaxis)
    ax.set_ylabel(ylabel=label_yaxis)
    title_heb_reversed = correct_heb_mirror_string(fig_title)
    ax.set_title(title_heb_reversed, fontsize=16)

    if is_x_rtl:
        x_tick_labels = ax.get_xticklabels()
        x_tick_labels = [x.get_text() for x in x_tick_labels]
        correct_ticks_labels = correct_heb_mirror_list(x_tick_labels)
        ax = plt.gca()
        ax.set_xticklabels(labels=correct_ticks_labels)

    plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
             rotation_mode="anchor", fontsize=6)

    plt.tight_layout()
    make_fullscreen()
    # plt.show(block=False)
    save_figure(figure_name=figure_name)


# Save folium map into designated folder
def save_folium_map(map_plot, file_name, output_folder="Output_files"):
    folium_map_folder = "map graphs"
    working_directory = os.getcwd()
    directory = working_directory + "\\" + output_folder + "\\" + folium_map_folder
    if not os.path.exists(directory):
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        os.chdir(output_folder)
        if not os.path.exists(folium_map_folder):
            os.mkdir(folium_map_folder)
        os.chdir(folium_map_folder)
    else:
        os.chdir(directory)
    map_plot.save(outfile=file_name + ".html")
    os.chdir(working_directory)

# Save plotly map into designated folder
# def save_plotly_map(map_plot, file_name, output_folder="Output_files"):
#     map_folder = "map graphs"
#     working_directory = os.getcwd()
#     directory = working_directory + "\\" + output_folder + "\\" + map_folder
#     if not os.path.exists(directory):
#         if not os.path.exists(output_folder):
#             os.mkdir(output_folder)
#         os.chdir(output_folder)
#         if not os.path.exists(map_folder):
#             os.mkdir(map_folder)
#         os.chdir(map_folder)
#     else:
#         os.chdir(directory)
#     map_plot.save(file_name + ".png")

# loop trough available colors for map
def color_looper(number):
    color = ["blue", "green", "purple", "orange", "darkred", "lightred", "beige", "darkblue", "darkgreen",
             "darkpurple", "lightblue", "lightgreen" ] # Not seen as well on this map tile "black", "gray", lightgray", "white", "cadetblue", "red", "pink"
    return [color[number % len(color)] if len(color)-1 < number else color[number]][0]

# Create plotly geographical map with size according to industry
def industry_size_map(data_list, data_values_list, industry_col):
    for ind, data_df in enumerate(data_list):
        gv_points = gv.Points(data_df, ['longitude', 'latitude'],
                                       ['IATA', 'city', 'passengers',
                                        'country', 'color'])
        tooltips = [('@YeshuvAtarSvivatiMenifa')]
        hover = HoverTool(tooltips=tooltips)
        airports_plot = (gvts.CartoEco * gv_points).opts(
            opts.Points(width=1200, height=700, alpha=0.3,
                        color=dim('color'), hover_line_color='black',
                        line_color='black', xaxis=None, yaxis=None,
                        tools=[hover], size="",
                        hover_fill_color=None, hover_fill_alpha=0.5))

# Create plotly geographical map with size according to industry
# def industry_size_map(data_list, data_values_list, industry_col):
#     for ind, data_df in enumerate(data_list):
#         fig = px.scatter_mapbox(data_df, lat='latitude', lon='longitude', size=industry_col, color="YeshuvAtarSvivatiMenifa",
#                                 color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
#         # fig = px.scatter_geo(data_df, lon = data_df['longitude'], lat = data_df['latitude'],
#         #                      hover_name="YeshuvAtarSvivatiMenifa", size=industry_col,
#         #                      projection="natural earth")
#         # fig.update_layout(
#         #     title=industry_col+"-"+data_values_list[ind],
#         #     geo=dict(
#         #         scope='israel',
#         #         showland=True,
#         #         landcolor="rgb(250, 250, 250)",
#         #         subunitcolor="rgb(217, 217, 217)",
#         #         countrycolor="rgb(217, 217, 217)",
#         #         countrywidth=0.5,
#         #         subunitwidth=0.5
#         #     ),
#         # )
#         fig.show()
#         save_plotly_map(map_plot=fig, file_name=industry_col+"-"+data_values_list[ind])

# Create folium map
def industry_map(data_list, data_values_list, industry_col):
    for ind, data_df in enumerate(data_list):
        # Create empty map
        map_f = folium.Map(
            # location=[31.0461, 34.8516], #Israel
            location=[data_df["latitude"].mean(), data_df["longitude"].mean()],
            tiles='cartodbpositron',
            zoom_start=8,
        )

        # Create legend through html
        # legend_html = '''
        #  <div style=”position: fixed;
        #  bottom: 50px; left: 50px; width: 1000px; height: 900px;
        #  border:2px solid grey; z-index:9999; font-size:14px;
        #  “>&nbsp; Cool Legend <br>
        #  '''
        # html_marker = '''
        #      &nbsp; {industry_name} &nbsp; <i class=”fa fa-map-marker fa-2x”
        #               style=”color:{marker_color}”></i><br>
        # '''

        # Loop to plot each data series separately with a different color and add it to legend

        color = color_looper(ind)
        # legend_html = legend_html + html_marker.format(industry_name=data_values_list[ind], marker_color=color)

        # The following lines only work for plotting all data points at once
        data_df.apply(
        lambda row: folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=5, fill=True,
                                        # Set fill to True
                                        fill_color=color,
                                        color=color, ).add_to(map_f), axis=1)

        # Finish legend and display it
        # html_end = "</div>"
        # legend_html = legend_html + html_end
        # map_f.get_root().html.add_child(folium.Element(legend_html))

        save_folium_map(map_plot=map_f, file_name=industry_col+"-"+data_values_list[ind])

    '''
     Map tileset to use. Can choose from this list of built-in tiles:
     ”OpenStreetMap”
     ”Stamen Terrain”,
     “Stamen Toner”,
     “Stamen Watercolor”
     ”CartoDB positron”,
     “CartoDB dark_matter”
     ”Mapbox Bright”, “Mapbox Control Room” (Limited zoom)
     ”Cloudmade” (Must pass API key)
     ”Mapbox” (Must pass API key)
     '''


# Create folium map - an attampt to plot each categpru with a diffrent color on the same map
# def industry_map(data, masks, data_values, industry_col):
#     # Create empty map
#     map_f = folium.Map(
#         # location=[31.0461, 34.8516], #Israel
#         location=[data["latitude"].mean(), data["longitude"].mean()],
#         tiles='cartodbpositron',
#         zoom_start=8,
#     )
#
#     # Create legend through html
#     legend_html = '''
#      <div style=”position: fixed;
#      bottom: 50px; left: 50px; width: 1000px; height: 900px;
#      border:2px solid grey; z-index:9999; font-size:14px;
#      “>&nbsp; Cool Legend <br>
#      '''
#     html_marker = '''
#          &nbsp; {industry_name} &nbsp; <i class=”fa fa-map-marker fa-2x”
#                   style=”color:{marker_color}”></i><br>
#     '''
#
#     # Loop to plot each data series separately with a different color and add it to legend
#     for ind, mask in enumerate(masks):
#         color = color_looper(ind)
#         legend_html = legend_html + html_marker.format(industry_name=data_values[ind], marker_color=color)
#
#     # The following lines plot each point individualy
#         mini_df = data.loc[mask[0], ["yeshuv", "latitude", "longitude"]]
#         for i in range(0, len(mini_df)):
#             folium.Marker([mini_df.iloc[i]['latitude'], mini_df.iloc[i]['longitude']],
#                           color=color).add_to(map_f)
#
#     # Finish legend and display it
#     html_end = "</div>"
#     legend_html = legend_html + html_end
#     map_f.get_root().html.add_child(folium.Element(legend_html))
#
#     save_folium_map(map_plot=map_f, file_name=industry_col)
#
#     '''
