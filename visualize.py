'''
    Analysis of Israel Pollutant Release and Transfer Register (PRTR)
    Copyright (C) 2020  Doreen S. Ben-Zvi, PhD

    Full license is locates in License.txt at project root folder.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import math
import os

import altair as alt
import altair_saver
import arabic_reshaper
import folium
import geoviews as gv
import geoviews.tile_sources as gvts
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from bidi import algorithm as bidialg
from bokeh.models import HoverTool
from geoviews import dim, opts

from data_cleaning import shorten_name


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


# Save matplotlib output_folder_name
def save_figure(figure_name, output_folder_name="Output_files"):
    working_directory = os.getcwd()
    if output_folder_name != "":
        if not os.path.exists(output_folder_name):
            os.mkdir(output_folder_name)
        os.chdir(output_folder_name)
    plt.savefig(fname=figure_name, bbox_inches='tight')
    plt.close()
    dir = os.getcwd()
    os.chdir(working_directory)
    return dir


# Compare log and non log y scales in one instance of accidental and non accidental emissions
def compare_for_presentation(dataframe, pv, col_by, col_name, col_of):
    if col_by == "TchumPeilutAtarSvivati" and dataframe["SugPlita"][0] == "מקור מים" and dataframe[col_of][
        0] == "חומרים אנאורגניים":
        fig, axes = plt.subplots(1, 2)
        title_heb = 'פליטה של חומרים אנאורגניים בתאונות ובשגרה למקור מים לפי מוצר - השוואת לוג'
        title_heb_corrected = correct_heb_mirror_string(title_heb)
        fig.suptitle(title_heb_corrected)

        for i, ax in enumerate(axes.flat):
            if i == 0:
                ax.set_title(correct_heb_mirror_string('ציר y רגיל'))
                label_yaxis = correct_heb_mirror_string("פליטה (Kg)")
                ax.set_ylabel(ylabel=label_yaxis)
                pv.plot.bar(log=False, stacked=False, ax=ax)
                correct_ticks_labels = correct_heb_mirror_list(pv.axes[0])
                ax.set_xticklabels(labels=correct_ticks_labels)
            elif i == 1:
                ax.set_title(correct_heb_mirror_string('ציר y לוגריתמי'))
                label_yaxis = correct_heb_mirror_string("פליטה (log Kg)")
                ax.set_ylabel(ylabel=label_yaxis)
                pv.plot.bar(log=True, stacked=False, ax=ax)
                correct_ticks_labels = correct_heb_mirror_list(pv.axes[0])
                ax.set_xticklabels(labels=correct_ticks_labels)
            label_xaxis = correct_heb_mirror_string(col_name)
            ax.set_xlabel(xlabel=label_xaxis)
            fig.autofmt_xdate()

        plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
                 rotation_mode="anchor", fontsize=6)
        # plt.tight_layout()
        make_fullscreen()
        plt.show(block=False)
        dir = save_figure(figure_name=title_heb)
        print("Figure with two sublots saved at " + str(dir))


# Bar plot comparing accidental and non accidental emissions
def accidents_with_non_acci(dataframes, col_by, col_of, title_template, col_name, output_folder_name, is_x_rtl=False,
                            is_log=False):
    if os.getcwd() != output_folder_name:
        os.chdir(output_folder_name)
    for dataframe in dataframes:
        # Arrange data columns and legend
        title_heb = title_template.format(dataframe[col_of][0], dataframe["SugPlita"][0], col_name)
        title_heb_reversed = correct_heb_mirror_string(title_heb)
        data_series = ['KamutPlitaLoBeTeunot', 'KamutPlitaBeTeunot']
        new_legend = correct_heb_mirror_list(['כמות פליטה בשגרה', 'כמות פליטה בתאונות'])
        pv = pd.pivot_table(data=dataframe, values=data_series, index=[col_by], aggfunc="sum")
        pv.dropna(axis=0, how='any', inplace=True)
        pv = pv.loc[~(pv == 0).all(axis=1)]

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
            dir = save_figure(figure_name=title_heb, output_folder_name=output_folder_name)
            print("Accident and Non-accident comparing graph saved at " + str(dir))
            compare_for_presentation(dataframe=dataframe, pv=pv, col_by=col_by, col_name=col_name, col_of=col_of)


# Bar plot displaying accidental or non accidental emissions
def accidents_or_non_acci(dataframes, col_by, col_of, title_template, col_name, data_series, is_x_rtl=False,
                          is_log=False):
    for dataframe in dataframes:
        # Arrange data columns and legend
        title_heb = title_template.format(dataframe[col_of][0], dataframe["SugPlita"][0], col_name)
        title_heb_reversed = correct_heb_mirror_string(title_heb)
        pv = pd.pivot_table(data=dataframe, values=data_series, index=[col_by], aggfunc="sum")
        pv.dropna(axis=0, how='any', inplace=True)
        pv = pv.loc[~(pv == 0).all(axis=1)]

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
            dir = save_figure(figure_name=title_heb, output_folder_name="")
            print("Accidental emmission graphs saved at " + str(dir))


# Petal Scatter plot with color indicating category and size indicating value
def multi_feat_scatter(data, filename, x_col, y_col, size_col, color_col, output_folder_name="Output_files"):
    working_directory = os.getcwd()
    if output_folder_name != "":
        if not os.path.exists(output_folder_name):
            os.mkdir(output_folder_name)
        os.chdir(output_folder_name)
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
    dir = os.getcwd()
    altair_saver.save(chart, filename + ".html")
    os.chdir(working_directory)
    print("Multi feature scatter plot saved at " + str(dir))


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
    dir = save_figure(figure_name=figure_name)
    print("Violin plot saved at " + str(dir))


# Save folium map into designated folder
def save_folium_map(map_plot, file_name, output_folder="Output_files"):
    folium_map_folder = "map graphs - dots"
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
    dir = os.getcwd()
    os.chdir(working_directory)
    return dir


# Save geoviews map into designated folder
def save_geoviews(map_plot, file_name, renderer, output_folder="Output_files"):
    map_folder = "map graphs - circles"
    working_directory = os.getcwd()
    directory = working_directory + "\\" + output_folder + "\\" + map_folder
    if not os.path.exists(directory):
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        os.chdir(output_folder)
        if not os.path.exists(map_folder):
            os.mkdir(map_folder)
        os.chdir(map_folder)
    else:
        os.chdir(directory)
    renderer.save(map_plot, file_name[0:40])
    dir = os.getcwd()
    os.chdir(working_directory)
    return dir


# loop trough available colors for folium map
def color_looper_folium(number):
    color = ["blue", "green", "purple", "orange", "darkred", "lightred", "darkblue", "darkgreen",
             "darkpurple", "lightblue",
             "lightgreen"]  # Not seen as well on this map tile "black", "gray", lightgray", "beige", "white", "cadetblue", "red", "pink"
    return [color[number % len(color)] if len(color) - 1 < number else color[number]][0]


# loop trough available colors for map
def color_looper_bokeh(number):
    color = ["aqua", "aqua", "blue", "blueviolet", "darkred", "cadetblue", "chartreuse", "coral", "cornflowerblue",
             "darkgoldenrod", "darkgreen", "darkmagenta", "darkorange", "darkorchid", "deeppink", "gold", "greenyellow",
             "lightcoral", "plum", "orange"]
    return [color[number % len(color)] if len(color) - 1 < number else color[number]][0]


# Create geoviews map with size according to industry
def industry_size_map(data_list, data_values_list, industry_col):
    for ind, data_df in enumerate(data_list):
        renderer = gv.renderer('bokeh')
        gv_points = gv.Points(data_df, ['longitude', 'latitude'],
                              [industry_col, 'YeshuvAtarSvivatiMenifa'])
        data_df.rename(columns={industry_col: ""})
        tooltips = [("Amount", "@" + industry_col),
                    ("Location", '@YeshuvAtarSvivatiMenifa')]
        hover = HoverTool(tooltips=tooltips)
        # map_plot =gvts.CartoLight.options(width=500, height=800, xaxis=None, yaxis=None, show_grid=False) * gv_points
        map_plot = (gvts.CartoLight * gv_points).opts(
            opts.Points(width=400, height=700, alpha=0.3,
                        hover_line_color='black', color=color_looper_bokeh(ind),
                        line_color='black', xaxis=None, yaxis=None,
                        tools=[hover], size=dim(industry_col) * 10,
                        hover_fill_color=None, hover_fill_alpha=0.5))
        dir = save_geoviews(map_plot=map_plot, file_name="map " + industry_col + "-" + data_values_list[ind],
                            renderer=renderer, output_folder="Output_files")
        print("Map plot saved at " + str(dir))


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


# Create plotly geographical map with size according to industry
# Plotly doesnt have a mapy of Israel so left unused
# def industry_size_map(data_list, data_values_list, industry_col):
#     for ind, data_df in enumerate(data_list):
#         fig = px.scatter_mapbox(data_df, lat='latitude', lon='longitude', size=industry_col, color="YeshuvAtarSvivatiMenifa",
#                                 color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
#         fig = px.scatter_geo(data_df, lon = data_df['longitude'], lat = data_df['latitude'],
#                              hover_name="YeshuvAtarSvivatiMenifa", size=industry_col,
#                              projection="natural earth")
#         fig.update_layout(
#             title=industry_col+"-"+data_values_list[ind],
#             geo=dict(
#                 scope='israel',
#                 showland=True,
#                 landcolor="rgb(250, 250, 250)",
#                 subunitcolor="rgb(217, 217, 217)",
#                 countrycolor="rgb(217, 217, 217)",
#                 countrywidth=0.5,
#                 subunitwidth=0.5
#             ),
#         )
#         fig.show()
#         save_plotly_map(map_plot=fig, file_name=industry_col+"-"+data_values_list[ind])

# Create folium map
# TODO: HTML labling doesn't work (commented out)
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

        color = color_looper_folium(ind)
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

        dir = save_folium_map(map_plot=map_f, file_name=industry_col + "-" + data_values_list[ind])
        print("Map plote saved at " + str(dir))

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


# plot waste using pandas.dataframe.plot()
def waste_graph(data):
    data = shorten_name(dataframe=data, cols=["ShemAtarSvivatiMenifa"], how_short=40)
    pv_factories = pd.pivot_table(data=data,
                                  values=["total_waste", "total_non_dangerous_waste", "total_dangerous_waste"],
                                  index=["ShemAtarSvivatiMenifa"], aggfunc=np.sum)
    pv_factories = pv_factories.reset_index()
    pv_factories = pv_factories.sort_values(by=["total_waste"], ascending=False)
    # Scaling
    pv_factories["total_waste"] = pv_factories["total_waste"].div(10 ** 9)
    pv_factories["total_non_dangerous_waste"] = pv_factories["total_non_dangerous_waste"].div(10 ** 9)
    pv_factories["total_dangerous_waste"] = pv_factories["total_dangerous_waste"].div(10 ** 9)
    # Plotting just highest polutents
    pv_factories = pv_factories[:10]
    pv_factories.plot(x="ShemAtarSvivatiMenifa", kind='bar', sharey=True, subplots=True, legend=False)

    # Adjust each plot in figure
    fig = plt.gcf()
    ax_list = fig.axes

    # Get max and min values from all branches to be used in all graphs
    # min_y = data[["total_waste", "total_non_dangerous_waste", "total_dangerous_waste"]].min().min()
    # max_y = data[["total_waste", "total_non_dangerous_waste", "total_dangerous_waste"]].max().max()
    for one_axis in ax_list:
        #     # one_axis.set_ylim(min_y, max_y)

        # Move legend to left outside of graph and remove box around it
        patches, labels = one_axis.get_legend_handles_labels()
        one_axis.legend(patches, labels, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

        # Remove x axis labels from all graphs but bottom one
        one_axis.axes.get_xaxis().set_visible(False)
        one_axis.set_title("")
        if one_axis is ax_list[0]:
            one_axis.set_title("Factories producing most waste")
        #
        if one_axis is ax_list[math.floor(len(ax_list) / 2)]:
            one_axis.axes.set_ylabel("Waste (10^9 kg)")
        #
        if one_axis is ax_list[-1]:
            x_tick_labels = one_axis.get_xticklabels()
            x_tick_labels = [x.get_text() for x in x_tick_labels]
            correct_ticks_labels = correct_heb_mirror_list(x_tick_labels)
            one_axis.axes.get_xaxis().set_visible(True)
            plt.setp(one_axis.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
            # ax = plt.gca()
            one_axis.set_xticklabels(labels=correct_ticks_labels)
            one_axis.axes.set_xlabel("Factory name")

    plt.tight_layout()
    make_fullscreen()
    # plt.show(block=False)
    dir = save_figure(figure_name="FactoriesWaste")
    print(str(dir))
