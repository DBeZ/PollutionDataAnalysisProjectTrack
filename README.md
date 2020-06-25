# Data analysis project - Industrial Pollution

PollutionDataAnalysisProjectTrack




# Data:
Uses Israel ministry of environmental protection Pollutant Release and Transfer Register (PRTR).
It contains structured Data, with Quantitative and Categorical entries.




# Purpose:

* Assess the reduction in which industries will have a great positive impact on pollution of various type.
* Infer whether accidents have a profound impact on pollution in certain industries.
* Identify Industrial geographical clusters which moving/reducing will have a significant difference on pollution in different areas in Israel.




# Project outline:

**1.** Data Cleaning

     Uses a non-graphic UI. Cleaned data is then pickled. If a pickled data file exists UI will not be called.
     Columns with low variability (less than two unique values) are removed.
     
    (1.2) Numeric columns description is displayed. 
    
    (1.3) Non-numeric columns description is displayed. 
    
    (1.4) All column names are displayed.
    
    (1.5) The type, unique value amount and a sample of of its values are displayed. 
    
    (1.6) Dialog asks whether to convert the column to int, bool, date (d/m/Y format), category or to record its name for future decision. 
          Column where conversion fails are also recorded for further exploration.
          
    (1.7) Columns containing NaNs are listed. These are not all with empty cells as empty strings are not identified.
 
    Specific column treatment: Comma removal from numeric values, accidental/non accidental/total emission calculated from data, non-dangerous waste column created. 
 
 
  
**2.** Bar plots of 10 factories which produce the most waste, dangerous and non-dangerous.


**3.** Multi-feature scatter plot comparing accidental and non-accidental emission using altair. y axis is industry field, x axis is a sub division of industry fields. Circle size denotes emission amount. 

Graphs saved as HTML file in subfolders of the output folder.

A non-graphic UI is called to determine the number of high outlier removal - a number is selected, graphs are saved and results is confirmed or the process is repeated with a new entered number.



**4.** Violin plots created for accidental and non-accidental emission in industry fields using seaborn. 

Optional: Create bar plots of all possible options of emission type and destination, with and without log y axis. 

Optional: Crate a bar plot comparing all possible options of emission type and destination, with logarithmic y axis. 

Optional: Create on two-graph plot (2 subplots) demonstrating the effect of y log scale on inorganic emissions to water sources (by product). 

Graphs saved as png files in the output folder.

Note- all optimal plots render by visibly maximizing figure window, causing a flickering affect. 



**5.** Gepoy converts Hebrew city names to latitude and longitude. Geolocation data is pickled into output folder. If a pickled data geolocation file exists it will be used instead of accessing the geolocation server.


**6.** Number of factories in each field plotted on map using geoviews. bokeh provides interactivity. Circle size indicates number of factories in the city. Circle color changes between graphs. Graphs saved as HTML in a subfolder of the output folder.

Optional: plotting using Folium, non-interactive map (no tooltips or different circle sizes). Circle color changes between graphs. Graphs saved as HTML in a    subfolder of the output folder.

# Extra notes:

Note - axis labels and tick labels are in Hebrew, labels are mirrored to allow for proper presentation. Some of them are shortened to an arbitrary length for display purposes. Others are shortened by dictionary.

Note - subtables for pivot are either masked or by creating a separate new table for each value in a given column (when the values are categories).


# Lisence:
Released under GNU Affero General Public License, see Lisence.txt or <https://www.gnu.org/licenses/>.

