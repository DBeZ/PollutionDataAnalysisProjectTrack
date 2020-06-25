# PollutionDataAnalysisProjectTrack
Data analysis project - of Industrial Pollution Database

Uses Israel ministry of environmental protection Pollutant Release and Transfer Register (PRTR).
It contains structured Data, with Quantitative and Categorical entries.

Purpose:
(1) Assess the reduction in which industries will have a great positive impact on pollution of various type.
(2) Infer whether accidents have a profound impact on pollution in certain industries.
(3) Identify Industrial geographical clusters which moving/reducing will have a significant difference on pollution in different areas in Israel.

Project outline:
(a) Data Cleaning. Uses a non-graphic UI. Cleaned data is then pickled. If a pickled data file exists UI will not be called.
  (a.1) Columns with low variability (less than two unique values) are removed.
  (a.2) Numeric columns description is displayed. 
  (a.3) Non-numeric columns description is displayed. 
  (a.4) All column names are displayed.
  (a.5) The type, unique value amount and a sample of of its values are displayed. 
  (a.6) Dialog asks whether to convert the column to int, bool, date (d/m/Y format), category or to record its name for future decision. 
        Column where conversion fails are also recorded for further exploration.
  (a.7) Columns containing NaNs are listed. These are not all with empty cells as empty strings are not identified.
 
 Specific column treatment: Comma removal from numeric values, accidental/non accidental/total emission calculated from data, non-dangerous waste column created. 
 
(b) Bar plots of 10 factories which produce the most waste, dangerous and non-dangerous.

() Multi-feature scatter plot comparing accidental and non-accidental emission using altair. y axis is industry field, x axis is a sub division of industry fields. Circle size denotes emission amount. 
Graphs saved as HTML file in subfolders of the output folder.
A non-graphic UI is called to determine the number of high outlier removal - a number is selected, graphs are saved and results is confirmed or the process is repeated with a new entered number.


() Violin plots created for accidental and non-accidental emission in industry fields using seaborn. 
Optional: Create bar plots of all possible options of emission type and destination, with and without log y axis. 
Optional: Crate a bar plot comparing all possible options of emission type and destination, with logarithmic y axis. 
Optional: Create on two-graph plot (2 subplots) demonstrating the effect of y log scale on inorganic emissions to water sources (by product). 
Graphs saved as png files in the output folder.
Note- all optimal plots render by visibly maximizing figure window, causing a flickering affect. 


() Gepoy converts Hebrew city names to latitude and longitude. Geolocation data is pickled into output folder. If a pickled data geolocation file exists it will be used instead of accessing the geolocation server.
() Number of factories in each field plotted on map using geoviews. bokeh provides interactivity. Circle size indicates number of factories in the city. Circle color changes between graphs. Graphs saved as HTML in a subfolder of the output folder.
Optional: plotting using Folium, non-interactive map (no tooltips or different circle sizes). Circle color changes between graphs. Graphs saved as HTML in a subfolder of the output folder.


Note - axis labels and tick labels are in Hebrew, labels are mirrored to allow for proper presentation. Some of them are shortened to an arbitrary length for display purposes.
Note - subtables for pivot are either masked or by creating a separate new table for each value in a given column (when the values are categories).

Released under GNU Affero General Public License, see Lisence.txt or <https://www.gnu.org/licenses/>.

