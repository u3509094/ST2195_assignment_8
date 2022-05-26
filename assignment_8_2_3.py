import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from PyPDF2 import PdfFileReader
pdfFileObject = open("Direction of Trade Statistics Yearbook, 2017.pdf", "rb")
pdfReader = PdfFileReader(pdfFileObject)

def extract_from_page(page):
    country_info = ""
    for i in page:
        # creating a page object
        pageObj = pdfReader.getPage(i)
        # extracting text from page
        country_info += pageObj.extractText()
    return country_info.split("\n")

def filter_g7(country, info):
    g7 = ["Canada", "France", "Germany", "Italy", "Japan", "United Kingdom", "United States"]
    country_g7_info = []
    for i in range(len(info)):
        if info[i] in g7:
            country_g7_info.append(country)
            country_g7_info.append(info[i])
            for m in range(i + 1, i + 4):
                if not info[m][0].isupper():
                    country_g7_info.append(info[m][4:])
                    country_g7_info[-1] = country_g7_info[-1].replace(",", "")
                    country_g7_info[-1] = country_g7_info[-1].replace(" ", ",")
                else:
                    break
    return country_g7_info

def filter_2015(info):
    billion_list = ["Germany", "United States"]
    info_copy = info.copy()
    for i in range(len(info_copy)):
        list = []
        if "," in info_copy[i]:
            list = info_copy[i].split(",")
            info_copy[i] = [float(list[4]), float(list[10])]
            if info_copy[0] in billion_list:
                info_copy[i][0] = info_copy[i][0] * 1000
                info_copy[i][1] = info_copy[i][1] * 1000
            info_copy[i][0] = int(info_copy[i][0])
            info_copy[i][1] = int(info_copy[i][1])
    return info_copy

def filter_2016(info):
    billion_list = ["Germany", "United States"]
    info_copy = info.copy()
    for i in range(len(info_copy)):
        list = []
        if "," in info_copy[i]:
            list = info_copy[i].split(",")
            info_copy[i] = [float(list[5]), float(list[11])]
            if info_copy[0] in billion_list:
                info_copy[i][0] = info_copy[i][0] * 1000
                info_copy[i][1] = info_copy[i][1] * 1000
            info_copy[i][0] = int(info_copy[i][0])
            info_copy[i][1] = int(info_copy[i][1])
    return info_copy

canada_info = extract_from_page(range(169, 173))
france_info = extract_from_page(range(279, 283))
germany_info = extract_from_page(range(297, 301))
italy_info = extract_from_page(range(366, 370))
japan_info = extract_from_page(range(373, 377))
uk_info = extract_from_page(range(696, 700))
us_info = extract_from_page(range(700, 704))

canada_info = filter_g7("Canada", canada_info)
france_info = filter_g7("France", france_info)
germany_info = filter_g7("Germany", germany_info)
italy_info = filter_g7("Italy", italy_info)
japan_info = filter_g7("Japan", japan_info)
uk_info = filter_g7("United Kingdom", uk_info)
us_info = filter_g7("United States", us_info)

#2016
canada_info_16 = filter_2016(canada_info)
france_info_16 = filter_2016(france_info)
germany_info_16 = filter_2016(germany_info)
italy_info_16 = filter_2016(italy_info)
japan_info_16 = filter_2016(japan_info)
uk_info_16 = filter_2016(uk_info)
us_info_16 = filter_2016(us_info)

canada_info_16 = pd.DataFrame(np.array(canada_info_16).reshape(6, 3))
france_info_16 = pd.DataFrame(np.array(france_info_16).reshape(6, 3))
germany_info_16 = pd.DataFrame(np.array(germany_info_16).reshape(6, 3))
italy_info_16 = pd.DataFrame(np.array(italy_info_16).reshape(6, 3))
japan_info_16 = pd.DataFrame(np.array(japan_info_16).reshape(6, 3))
uk_info_16 = pd.DataFrame(np.array(uk_info_16).reshape(6, 3))
us_info_16 = pd.DataFrame(np.array(us_info_16).reshape(6, 3))

g7_info_16 = pd.concat([canada_info_16, france_info_16, germany_info_16, italy_info_16, japan_info_16, uk_info_16, us_info_16])
g7_info_16.columns = ["Country 1", "Country 2", "Export"]
g7_info_16["Import"] = ""
g7_info_16.reset_index(drop = True, inplace = True)
for i in range(len(g7_info_16.index)):
    g7_info_16.loc[i, "Import"] = g7_info_16.loc[i, "Export"][1]
    g7_info_16.loc[i, "Export"] = g7_info_16.loc[i, "Export"][0]
g7_info_16["Net Export"] = g7_info_16["Export"] - g7_info_16["Import"]
g7_info_16.to_csv("g7_16.csv")

del canada_info_16
del france_info_16
del germany_info_16
del italy_info_16
del japan_info_16
del uk_info_16
del us_info_16

#Network Visualisation
G = nx.Graph()
for index, row in g7_info_16.iterrows():
    G.add_edge(row["Country 1"], row["Country 2"], weight = row["Net Export"])

#Spring Layout
plt.subplots(figsize = (10, 10))
pos = nx.spring_layout(G)
nx.draw(G, pos = pos, font_size = 9)
nx.draw_networkx_labels(G, pos = pos, font_size = 12)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos = pos, edge_labels = edge_labels)
plt.tight_layout()
plt.axis("off");
plt.show()

#Random Layout
plt.subplots(figsize = (10, 10))
pos = nx.random_layout(G)
nx.draw(G, pos = pos, font_size = 9)
nx.draw_networkx_labels(G, pos = pos, font_size = 12)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos = pos, edge_labels = edge_labels)
plt.tight_layout()
plt.axis("off");
plt.show()

#Circular Layout
plt.subplots(figsize = (10, 10))
pos = nx.circular_layout(G)
nx.draw(G, pos = pos, font_size = 9)
nx.draw_networkx_labels(G, pos = pos, font_size = 12)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos = pos, edge_labels = edge_labels)
plt.tight_layout()
plt.axis("off");
plt.show()

#Circular Layout with MultiEdges
G = nx.MultiDiGraph()
weights = []
weights_position = 0
for index, row in g7_info_16.iterrows():
    G.add_edge(row["Country 1"], row["Country 2"], weight = row["Net Export"])
    weights.append(row["Net Export"] / 50000)

plt.subplots(figsize = (10, 10))
pos = nx.circular_layout(G)
for edge in G.edges(data=True):
    nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], width = weights[weights_position], arrowsize = 15, connectionstyle = "arc3, rad = 0.25")
    weights_position += 1
nx.draw_networkx_nodes(G, pos = pos)
nx.draw_networkx_labels(G, pos = pos, font_size = 12)
plt.tight_layout()
plt.axis("off");
plt.show()

#2015
canada_info_15 = filter_2015(canada_info)
france_info_15 = filter_2015(france_info)
germany_info_15 = filter_2015(germany_info)
italy_info_15 = filter_2015(italy_info)
japan_info_15 = filter_2015(japan_info)
uk_info_15 = filter_2015(uk_info)
us_info_15 = filter_2015(us_info)

canada_info_15 = pd.DataFrame(np.array(canada_info_15).reshape(6, 3))
france_info_15 = pd.DataFrame(np.array(france_info_15).reshape(6, 3))
germany_info_15 = pd.DataFrame(np.array(germany_info_15).reshape(6, 3))
italy_info_15 = pd.DataFrame(np.array(italy_info_15).reshape(6, 3))
japan_info_15 = pd.DataFrame(np.array(japan_info_15).reshape(6, 3))
uk_info_15 = pd.DataFrame(np.array(uk_info_15).reshape(6, 3))
us_info_15 = pd.DataFrame(np.array(us_info_15).reshape(6, 3))

g7_info_15 = pd.concat([canada_info_15, france_info_15, germany_info_15, italy_info_15, japan_info_15, uk_info_15, us_info_15])
g7_info_15.columns = ["Country 1", "Country 2", "Export"]
g7_info_15["Import"] = ""
g7_info_15.reset_index(drop = True, inplace = True)
for i in range(len(g7_info_15.index)):
    g7_info_15.loc[i, "Import"] = g7_info_15.loc[i, "Export"][1]
    g7_info_15.loc[i, "Export"] = g7_info_15.loc[i, "Export"][0]
g7_info_15["Net Export"] = g7_info_15["Export"] - g7_info_15["Import"]
g7_info_15.to_csv("g7_15.csv")

del canada_info_15
del france_info_15
del germany_info_15
del italy_info_15
del japan_info_15
del uk_info_15
del us_info_15

#Network Visualisation
G = nx.Graph()
for index, row in g7_info_15.iterrows():
    G.add_edge(row["Country 1"], row["Country 2"], weight = row["Net Export"])

#Circular Layout with MultiEdges
G = nx.MultiDiGraph()
weights = []
weights_position = 0
for index, row in g7_info_15.iterrows():
    G.add_edge(row["Country 1"], row["Country 2"], weight = row["Net Export"])
    weights.append(row["Net Export"] / 50000)

plt.subplots(figsize = (10, 10))
pos = nx.circular_layout(G)
for edge in G.edges(data=True):
    nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], width = weights[weights_position], arrowsize = 15, connectionstyle = "arc3, rad = 0.25")
    weights_position += 1
nx.draw_networkx_nodes(G, pos = pos)
nx.draw_networkx_labels(G, pos = pos, font_size = 12)
plt.tight_layout()
plt.axis("off");
plt.show()