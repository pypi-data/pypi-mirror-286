import warnings
#warnings.filterwarnings("ignore", category=UserWarning, module='nxviz')
# Suppress specific UserWarning about no data for colormapping
warnings.filterwarnings('ignore', message="No data for colormapping provided via 'c'. Parameters 'cmap' will be ignored")

#import nxviz as nv
#from nxviz import annotate

import matplotlib as mpl
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd
from IPython.display import Image, display
import requests
import io
import re
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
from io import BytesIO
import json
import os
import math
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.path import Path
import matplotlib.patches as patches
import pathlib
from collections import Counter
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx
mpl.rcParams['font.family'] = "monospace"  # change default font family


# def plot_nv(G, sigPartition, min_comm_size=3, plot_dir='.', legend=True, kind='ArcPlots', show=True, background='transparent'):
#
#     pathlib.Path(plot_dir + "/" + kind + "/").mkdir(parents=True, exist_ok=True)
#
#     community_sizes = Counter(sigPartition.values())
#
#     # Identify small communities
#     small_communities = [comm for comm, size in community_sizes.items() if size < min_comm_size]
#
#     # Remove genes belonging to small communities from sigPartition
#     sigPartition = {gene: comm for gene, comm in sigPartition.items() if comm not in small_communities and comm != -1}
#
#     # Identify nodes to remove: those in small communities or in the -1 community
#     nodes_to_remove = [node for node, comm in G.nodes(data='community') if comm in small_communities or comm == -1]
#     G_trunc = G.copy()
#     G_trunc.remove_nodes_from(nodes_to_remove)
#
#     if len(set(sigPartition.values())) > 12:
#         # Sort communities by size and keep only the 12 largest
#         largest_communities = sorted(community_sizes, key=community_sizes.get, reverse=True)[:12]
#         removed_communities = set(sigPartition.values()) - set(largest_communities)
#
#         # Truncate G to include only nodes from the 12 largest communities
#         nodes_to_remove = [node for node, comm in sigPartition.items() if comm not in largest_communities]
#         G_trunc.remove_nodes_from(nodes_to_remove)
#
#         print(f"G has been truncated to include only the 12 largest communities. Communities removed: {removed_communities}")
#
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#
#     # Step 1: Check if any edge has a weight > 1
#     weight_greater_than_one = any(edge_data.get('weight', 0) > 1 for _, _, edge_data in G_trunc.edges(data=True))
#
#     # Step 2: If no edge has weight > 1, multiply all weights by 1000
#     if not weight_greater_than_one:
#         for u, v, edge_data in G_trunc.edges(data=True):
#             edge_data['weight'] = edge_data.get('weight', 0) * 1000
#             # Update the edge with the new weight
#             G_trunc[u][v]['weight'] = edge_data['weight']
#
#     if kind == 'ArcPlots':
#         g = nv.arc(G_trunc, node_color_by="community", group_by="community", edge_color_by="weight", edge_alpha_by="weight")
#         nv.annotate.arc_group(G_trunc, group_by="community")
#
#     elif kind == 'CircosPlots':
#         g = nv.circos(G_trunc, node_color_by="community", group_by="community", edge_color_by="weight",
#                       edge_alpha_by="weight")
#         nv.annotate.circos_group(G_trunc, group_by="community")
#
#     g.get_figure().set_size_inches(10, 10)
#
#     plt.tight_layout()
#     plt.autoscale()
#
#     if legend:
#         # Get edge weights
#         weights = np.array([float(w) for w in nx.get_edge_attributes(G_trunc, 'weight').values()])
#         # in case something with the weights went wrong and they are 0-1 scaled
#         if all([num < 1 for num in weights]):
#             weights = [w * 1000 for w in weights]
#
#         # Get min and max values
#         min_wt = np.min(weights)
#         max_wt = np.max(weights)
#
#         # Create four evenly spaced values in this range
#         # Make sure they are integers and divisible by 50
#         legend_values = np.linspace(min_wt, max_wt, 4)
#         legend_values = (np.round(legend_values / 50) * 50).astype(np.int64)
#
#         cmap = plt.cm.viridis
#         custom_lines = [Line2D([0], [0], color=cmap(i / 3.), lw=6) for i in range(4)]
#         ax.legend(custom_lines, legend_values, title="Score")
#
#     file_name = plot_dir + "/" + kind + "/PartitionedNetwork.png"
#     print("Saving network plots to %s" % file_name)
#     change_background_color(plt.gcf(), plt.gca(), background)
#
#     plt.savefig(file_name, dpi=300, bbox_inches='tight')
#     if show:
#         plt.show()
#     plt.close()


def create_circos_plot(G, partition):
    sorted_nodes = sorted(G.nodes(), key=lambda n: partition[n])
    node_angles = {node: i * 2 * np.pi / len(G) for i, node in enumerate(sorted_nodes)}

    unique_communities = sorted(set(partition.values()))
    color_map = plt.colormaps['tab20']
    community_colors = {comm: color_map(i / len(unique_communities)) for i, comm in enumerate(unique_communities)}

    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_aspect('equal')

    # Node placement and labeling
    node_radius = 1.0
    node_label_radius = 1.05
    for node in sorted_nodes:
        angle = node_angles[node]
        x, y = node_radius * np.cos(angle), node_radius * np.sin(angle)
        color = community_colors[partition[node]]
        ax.scatter(x, y, c=[color], s=100, zorder=2)

        label_angle = angle
        if not 0.5 * np.pi <= angle < 1.5 * np.pi:
            ha, va = 'left', 'center'
            label_angle = angle
        else:
            ha, va = 'right', 'center'
            label_angle = angle + np.pi

        label_x = node_label_radius * np.cos(angle)
        label_y = node_label_radius * np.sin(angle)

        ax.text(label_x, label_y, node, rotation=np.degrees(label_angle),
                ha=ha, va=va, rotation_mode='anchor', fontsize=10)

    # Edge drawing
    max_weight = max(d['weight'] for _, _, d in G.edges(data=True))
    for u, v, data in G.edges(data=True):
        start_angle = node_angles[u]
        end_angle = node_angles[v]
        start = node_radius * np.array([np.cos(start_angle), np.sin(start_angle)])
        end = node_radius * np.array([np.cos(end_angle), np.sin(end_angle)])

        angle_diff = min((end_angle - start_angle) % (2 * np.pi), (start_angle - end_angle) % (2 * np.pi))

        max_curve_angle = np.pi / 2
        curvature_factor = max(0, 1 - angle_diff / max_curve_angle)
        curvature_factor = curvature_factor ** 2.5

        mid_angle = (start_angle + end_angle) / 2
        if mid_angle > np.pi:
            mid_angle -= 2 * np.pi

        base_mid_radius = node_radius * 0.5
        max_mid_radius = node_radius * .95
        mid_radius = base_mid_radius + (max_mid_radius - base_mid_radius) * (1 - curvature_factor)

        if partition[u] == partition[v]:
            mid_radius *= max(0.7, 1 - angle_diff / np.pi)

        control = mid_radius * np.array([np.cos(mid_angle), np.sin(mid_angle)])

        verts = [
            (start[0], start[1]),
            (control[0], control[1]),
            (end[0], end[1]),
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE3,
            Path.CURVE3,
        ]

        path = Path(verts, codes)

        line_width = 0.5 + (data['weight'] / max_weight) * 4
        color_u = community_colors[partition[u]]
        color_v = community_colors[partition[v]]
        edge_color = np.mean([color_u, color_v], axis=0)

        patch = patches.PathPatch(path, facecolor='none', edgecolor=edge_color,
                                  lw=line_width, alpha=0.3, zorder=1)
        ax.add_patch(patch)

    # Community arcs and labels
    community_radius = 1.3
    community_label_radius = 1.4
    for comm in unique_communities:
        comm_nodes = [n for n in sorted_nodes if partition[n] == comm]
        if comm_nodes:
            start_angle = node_angles[comm_nodes[0]]
            end_angle = node_angles[comm_nodes[-1]]
            if end_angle < start_angle:
                end_angle += 2 * np.pi
            mid_angle = (start_angle + end_angle) / 2

            arc = mpatches.Arc((0, 0), 2 * community_radius, 2 * community_radius,
                               theta1=np.degrees(start_angle),
                               theta2=np.degrees(end_angle),
                               color=community_colors[comm], linewidth=2)
            ax.add_patch(arc)

            label_angle = mid_angle
            if not 0.5 * np.pi <= mid_angle < 1.5 * np.pi:
                ha, va = 'left', 'center'
                label_angle = mid_angle
            else:
                ha, va = 'right', 'center'
                label_angle = mid_angle + np.pi

            label_x = community_label_radius * np.cos(mid_angle)
            label_y = community_label_radius * np.sin(mid_angle)

            ax.text(label_x, label_y, f'Comm {comm}', rotation=np.degrees(label_angle),
                    ha=ha, va=va, rotation_mode='anchor', fontsize=12, fontweight='bold')

    # Add legend for edge weights
    weight_legend = []
    for weight in [max_weight * .25, max_weight * 0.5, max_weight * 0.75, max_weight]:
        line_width = 0.5 + (weight / max_weight) * 4
        weight_legend.append(mlines.Line2D([], [], color='gray', linewidth=line_width,
                                           label=f'{weight:.2f}'))

    ax.legend(handles=weight_legend, title='Score', loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')

    plt.tight_layout()

    return fig, ax


def plot_circos(G, sigPartition, min_comm_size=3, plot_dir='.', legend=True, show=True, background='transparent'):
    pathlib.Path(plot_dir + "/CircosPlots/").mkdir(parents=True, exist_ok=True)

    community_sizes = Counter(sigPartition.values())

    # Identify small communities
    small_communities = [comm for comm, size in community_sizes.items() if size < min_comm_size]

    # Remove genes belonging to small communities from sigPartition
    sigPartition = {gene: comm for gene, comm in sigPartition.items() if comm not in small_communities and comm != -1}

    # Identify nodes to remove: those in small communities or in the -1 community
    nodes_to_remove = [node for node, comm in G.nodes(data='community') if comm in small_communities or comm == -1]
    G_trunc = G.copy()
    G_trunc.remove_nodes_from(nodes_to_remove)

    # Step 1: Check if any edge has a weight > 1
    weight_greater_than_one = any(edge_data.get('weight', 0) > 1 for _, _, edge_data in G_trunc.edges(data=True))

    # Step 2: If no edge has weight > 1, multiply all weights by 1000
    if not weight_greater_than_one:
        for u, v, edge_data in G_trunc.edges(data=True):
            edge_data['weight'] = edge_data.get('weight', 0) * 1000
            # Update the edge with the new weight
            G_trunc[u][v]['weight'] = edge_data['weight']

    # Create the circos plot
    fig, ax = create_circos_plot(G_trunc, sigPartition)

    # Save the plot
    file_name = plot_dir + "/CircosPlots/PartitionedNetwork.png"
    change_background_color(fig, ax, background)
    fig.savefig(file_name, dpi=300, bbox_inches='tight')
    print(f"Circos plot saved as {file_name}")

    # Add legend if requested
    if legend:
        legend_fig, legend_ax = plt.subplots(figsize=(6, 4))
        weights = np.array([float(w) for w in nx.get_edge_attributes(G_trunc, 'weight').values()])

        # in case something with the weights went wrong and they are 0-1 scaled
        if all([num < 1 for num in weights]):
            weights = [w * 1000 for w in weights]

        min_wt = np.min(weights)
        max_wt = np.max(weights)

        legend_values = np.linspace(min_wt, max_wt, 4)
        legend_values = (np.round(legend_values / 50) * 50).astype(np.int64)

        cmap = plt.cm.viridis
        custom_lines = [Line2D([0], [0], color=cmap(i / 3.), lw=6) for i in range(4)]
        legend_ax.legend(custom_lines, legend_values, title="Score")

        change_background_color(legend_fig, legend_ax, background)
        legend_fig.savefig(plot_dir + "/CircosPlots/Legend.png", dpi=300, bbox_inches='tight')
        plt.close(legend_fig)

    if show:
        plt.show()
    else:
        plt.close(fig)



def weighted_set_cover(df, topN=None, category=None, description=None):
    """
    Performs a greedy weighted set cover algorithm on a DataFrame and returns a reduced DataFrame
    that includes selected pathways based on the smallest False Discovery Rate (fdr) and covering all unique genes.

    Args:
        df (pd.DataFrame): DataFrame with columns 'inputGenes', 'category', 'fdr'.
                           Optional 'description' column.
        topN (int, optional): Maximum number of pathways to return. Defaults to None, indicating all pathways are considered.
        category (str, optional): Filter pathways by a specific category.
        description (str, optional): Filter pathways by matching a substring in the description.

    Returns:
        pd.DataFrame: Reduced DataFrame containing only the selected pathways.
    """

    # Filter DataFrame based on category and description criteria
    if category:
        df = df[df['category'] == category]
    if description:
        df = df[df['description'].str.contains(description, na=False)]


    # Sort DataFrame by 'fdr' in ascending order to prioritize significant pathways first
    df.sort_values('fdr', ascending=True, inplace=True)

    # Handle cases where there may be no genes to work with
    if df.empty or 'inputGenes' not in df.columns or df['inputGenes'].isnull().all():
        warnings.warn("No significant pathways found; the DataFrame is empty or improperly formatted.")
        return df.iloc[[]]  # Return an empty DataFrame with the same structure

    try:
        # Initialize sets for the greedy algorithm
        all_genes = set.union(*df['inputGenes'].dropna().apply(set))
    except TypeError as e:
        warnings.warn(f"Failed to initialize gene sets: {str(e)}")
        return df.iloc[[]]

    selected_indices = []
    covered_genes = set()

    # Iterate through the pathways in sorted order
    for idx, row in df.iterrows():
        pathway_genes = set(row['inputGenes'])

        # Calculate the number of new genes this pathway would cover
        new_genes = pathway_genes - covered_genes
        if new_genes:
            # Update the covered genes set
            covered_genes.update(new_genes)
            selected_indices.append(idx)

            # Check if all genes are covered or if we have selected enough pathways
            if len(covered_genes) == len(all_genes) or (topN is not None and len(selected_indices) >= topN):
                break

    # Return the DataFrame containing only the selected pathways
    return df.loc[selected_indices]

def plotWordclouds(funcAnnots, categories='default', plot_dir='.', show=True, background='transparent', weightedSetCover=False):
    if not isinstance(categories, str):
        pass
    elif categories.lower() == 'pathways':
        categories = ["KEGG", "WikiPathways", "RCTM"]
    elif categories.lower() == 'default':
        categories = ["Process", "Function", "Component", "KEGG", "WikiPathways", "RCTM"]
    elif categories.lower() == 'no_pmid':
        categories = ["Process", "Function", "Component", "KEGG", "WikiPathways", "RCTM",
                      "NetworkNeighborAL", "SMART", "COMPARTMENTS", "Keyword", "TISSUES", "Pfam",
                      "MPO", "InterPro", ]
    elif categories.lower() == 'no_go':
        categories = ["KEGG", "WikiPathways", "RCTM",
                      "NetworkNeighborAL", "SMART", "COMPARTMENTS", "Keyword", "TISSUES", "Pfam",
                      "MPO", "InterPro", ]
    # gather all categories
    elif categories.lower() == 'all':
        categories = set()
        for df in funcAnnots.values():
            categories.update(df['category'].unique())
        categories = list(categories)

    pathlib.Path(plot_dir + "/WordClouds/").mkdir(parents=True, exist_ok=True)

    # Create a color map
    colors = sns.color_palette('Dark2', len(categories)).as_hex()
    color_map = dict(zip(categories, colors))

    for commNum, df in funcAnnots.items():
        if categories != 'all':
            df = df[df['category'].isin(categories)]

        if weightedSetCover:
            df = weighted_set_cover(df.copy())

        # Create a word cloud
        if background == 'transparent':
            wc = WordCloud(background_color=None, mode="RGBA", width=1600, height=800)
        else:
            wc = WordCloud(background_color=background, width=1600, height=800)
        weights = dict(zip(df['description'], -np.log10(df['fdr'])))
        try:
            wc.generate_from_frequencies(weights)
        except ValueError:
            # Generate a word cloud with a placeholder message, ensuring uniform color and size
            placeholder_message = 'No significant functional enrichment found for the specified databases'
            # Create a dictionary with the placeholder message as the key and a frequency of 1
            placeholder_freq = {placeholder_message: 1}
            # Generate the word cloud from the single "word" (our message)
            wc.generate_from_frequencies(placeholder_freq)
            # Optionally, set a uniform color for the message
            wc.recolor(color_func=lambda *args, **kwargs: "black")  # Use any color you prefer

        # Recolor the words
        def color_func(word, *args, **kwargs):
            category = df.loc[df['description'] == word, 'category'].values[0]
            return color_map[category]

        wc.recolor(color_func=color_func)

        # Display the word cloud
        plt.figure(commNum)
        plt.gcf().set_size_inches(15,8)
        plt.title(f'Community {commNum}: Functional Annotation')
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')

        # Create legend
        patches = [mpatches.Patch(color=color, label=category) for category, color in color_map.items()]
        plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')

        change_background_color(plt.gcf(), plt.gca(), background)

        file_name = plot_dir + "/WordClouds/community " + str(commNum) + "'s_wordcloud.png"
        print("Saving word clouds to %s" % file_name)

        plt.savefig(file_name, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()

def change_background_color(fig, ax, background):
    # Set the entire figure background color
    if background == 'transparent':
        fig.patch.set_alpha(0)  # Make the background of the figure transparent
        # For the subplots, in case you want them transparent as well
        ax.patch.set_alpha(0)
    else:
        # Convert color name or hex to RGBA tuple
        if isinstance(background, str):
            # Simple conversion for known colors, extend this as needed
            color_converter = {'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0)}
            new_background = color_converter.get(background.lower(), None)  # Default None if color is unknown
            if background.startswith('#'):  # For hex colors
                # Directly use the hex color for the facecolor
                new_background = background
        else:
            new_background = background  # Assuming background is already an RGBA tuple or hex color

        if new_background:
            fig.patch.set_facecolor(new_background)
            # Also set subplot backgrounds if needed
            ax.set_facecolor(new_background)

def plotPPI(PPIGraph, full_network=False, show=True, background='transparent'):
    pathlib.Path(PPIGraph.plot_dir + "/PPI_networks/").mkdir(parents=True, exist_ok=True)

    if PPIGraph.physical:
        network_type = "physical"
    else:
        network_type = "functional"

    string_api_url = "https://string-db.org/api"
    output_format = "image"
    method = "network"

    request_url = "/".join([string_api_url, output_format, method])

    if full_network:
        # add code for plotting the full network


        params = {
            "identifiers": "%0d".join(PPIGraph.gene_list),  # your protein
            "species": PPIGraph.organism,  # species NCBI identifier
            "network_flavor": "actions",  # show confidence links
            "caller_identity": "comet",  # your app name
            "required_score": str(PPIGraph.min_score),
            "network_type": network_type  # network type
        }

        response = requests.post(request_url, data=params)

        file_name = PPIGraph.plot_dir + "/PPI_networks/full_network.png"
        print("Saving interaction network to %s" % file_name)

        change_background_color(plt.gcf(), plt.gca(), background)

        with open(file_name, 'wb') as fh:
            fh.write(response.content)

        if show:
            image = Image.open(file_name)
            display(image)
        plt.close()


    else:

        # create dict of commNum: all comm genes
        allCommGeneSets = dict()
        for commNum in pd.Series(PPIGraph.partition.values()).sort_values().unique():
            commGeneSet = [k for k, v in PPIGraph.partition.items() if v == commNum]
            allCommGeneSets[commNum] = commGeneSet

        for commNum, commGeneSet in allCommGeneSets.items():

            # skip if community is too small
            if len(commGeneSet) < PPIGraph.min_comm_size:
                continue

            params = {
                "identifiers": "%0d".join(commGeneSet),  # your protein
                "species": PPIGraph.organism,  # species NCBI identifier
                "network_flavor": "actions",  # show confidence links
                "caller_identity": "comet",  # your app name
                "required_score": str(PPIGraph.min_score),
                "network_type": network_type  # network type
            }

            response = requests.post(request_url, data=params)

            file_name = PPIGraph.plot_dir + "/PPI_networks/community " + str(commNum) + "'s_network.png"
            print("Saving interaction network to %s" % file_name)

            change_background_color(plt.gcf(), plt.gca(), background)

            with open(file_name, 'wb') as fh:
                fh.write(response.content)

            if show:
                image = Image.open(file_name)
                display(image)
            plt.close()

def plotWordCloudsPPI(PPIGraph, categories='default', full_network = False, show=True, background='transparent', weightedSetCover=False):
    if type(categories) != str:
        pass
    elif categories.lower() == 'pathways':
        categories = ["KEGG", "WikiPathways", "RCTM"]
    elif categories.lower() == 'default':
        categories = ["Process", "Function", "Component", "KEGG", "WikiPathways", "RCTM"]
    elif categories.lower() == 'no_pmid':
        categories = ["Process", "Function", "Component", "KEGG", "WikiPathways", "RCTM",
                      "NetworkNeighborAL", "SMART", "COMPARTMENTS", "Keyword", "TISSUES", "Pfam",
                      "MPO", "InterPro", ]
    elif categories.lower() == 'no_go':
        categories = ["KEGG", "WikiPathways", "RCTM",
                      "NetworkNeighborAL", "SMART", "COMPARTMENTS", "Keyword", "TISSUES", "Pfam",
                      "MPO", "InterPro", ]

    # gather all categories
    elif categories.lower() == 'all':
        categories = set()
        if full_network:
            for df in PPIGraph.func_annotation_full_network.values():
                categories.update(df['category'].unique())
        else:
            for df in PPIGraph.func_annotation.values():
                categories.update(df['category'].unique())

    pathlib.Path(PPIGraph.plot_dir + "/WordCloudPPI_networks/").mkdir(parents=True, exist_ok=True)

    if PPIGraph.physical:
        network_type = "physical"
    else:
        network_type = "functional"

    # Create a color map
    colors = sns.color_palette('Dark2', len(categories)).as_hex()
    color_map = dict(zip(categories, colors))

    string_api_url = "https://string-db.org/api"
    output_format = "image"
    method = "network"

    request_url = "/".join([string_api_url, output_format, method])

    if full_network:
        allCommGeneSets = {'Full Network':[n for n in PPIGraph.network.nodes]}
        # set funcAnnots accordingly
        funcAnnots = PPIGraph.func_annotation_full_network.copy()
    else:
        # create dict of commNum: all comm genes
        allCommGeneSets = dict()
        for commNum in pd.Series(PPIGraph.partition.values()).sort_values().unique():
            commGeneSet = [k for k, v in PPIGraph.partition.items() if v == commNum]
            allCommGeneSets[commNum] = commGeneSet
        # set funcAnnots accordingly
        funcAnnots = PPIGraph.func_annotation.copy()

    for commNum, df in funcAnnots.items():
        # PPI network part
        commGeneSet = allCommGeneSets[commNum]

        # skip if community is too small
        if len(commGeneSet) < PPIGraph.min_comm_size:
            continue

        df = df[df['category'].isin(categories)]

        if weightedSetCover:
            df = weighted_set_cover(df.copy())

        # Create a word cloud
        if background == 'transparent':
            wc = WordCloud(background_color=None, mode="RGBA", width=1600, height=800, )
        else:
            wc = WordCloud(background_color=background, width=1600, height=800, )

        weights = dict(zip(df['description'], -np.log10(df['fdr'])))
        try:
            wc.generate_from_frequencies(weights)

            # Recolor the words
            def color_func(word, *args, **kwargs):
                category = df.loc[df['description'] == word, 'category'].values[0]
                return color_map[category]

            wc.recolor(color_func=color_func)

        except ValueError:
            # Generate a word cloud with a placeholder message, ensuring uniform color and size
            placeholder_message = 'No significant functional enrichment found for the specified databases'
            # Create a dictionary with the placeholder message as the key and a frequency of 1
            placeholder_freq = {placeholder_message: 1}
            # Generate the word cloud from the single "word" (our message)
            wc.generate_from_frequencies(placeholder_freq)
            # Optionally, set a uniform color for the message
            wc.recolor(color_func=lambda *args, **kwargs: "black")  # Use any color you prefer

        params = {
            "identifiers": "%0d".join(commGeneSet),  # your protein
            "species": PPIGraph.organism,  # species NCBI identifier
            "network_flavor": "actions",  # show confidence links
            "caller_identity": "comet",  # your app name
            "required_score": str(PPIGraph.min_score),
            "network_type": network_type  # network type
        }

        response = requests.post(request_url, data=params)

        # Create a figure with two subplots (1 row, 2 columns)
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        # Display the image in the first subplot
        img = mpimg.imread(io.BytesIO(response.content))
        axs[0].imshow(img)
        axs[0].axis('off')  # Hide the axes on the image plot

        # Display the word cloud
        # plt.figure(i)
        # plt.title(f'Community {i}: Functional Annotation')
        axs[1].imshow(wc)
        axs[1].axis('off')
        axs[1].set_title(f'Community {commNum}: Functional Annotation')

        # Create legend
        patches = [mpatches.Patch(color=color, label=category) for category, color in color_map.items()]
        axs[1].legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')

        file_name = PPIGraph.plot_dir + "/WordCloudPPI_networks/community " + str(commNum) + "'s_ppi_wordcloud.png"

        change_background_color(fig, axs[0], background)
        change_background_color(fig, axs[1], background)

        print("Saving PPI word clouds to %s" % file_name)
        plt.savefig(file_name, dpi=300, bbox_inches='tight')

        if show:
            plt.show()
        plt.close()

def visualize_KEGG(pathway_id, gene_reg_dict, organism=9606, plot_dir=".", transparency=.5, community=None, show=True, background='transparent', suffix=''):

    if organism == 'human':
        organism = 9606
    elif organism == 'mouse':
        organism = 10090

    # Path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), '.', 'data', 'org_gene_to_kegg.json')
    with open(json_path, 'r') as file:
        gene_kegg_dict = json.load(file)


    # check keys of org_gene_to_kegg.json
    if str(organism) in gene_kegg_dict.keys():
        # Creating a new dict for kegg_id:reg
        kegg_reg_dict = {}

        for gene, kegg_ids in gene_kegg_dict[str(organism)].items():
            reg = gene_reg_dict.get(gene)
            if reg is not None:
                if len(kegg_ids) > 1:
                    print(f"Mapping {gene} to " + ", ".join(kegg_ids))
                for kegg_id in kegg_ids:
                    # Initialize the list if the kegg_id is encountered for the first time
                    if kegg_id not in kegg_reg_dict:
                        kegg_reg_dict[kegg_id] = []
                    # Append the reg value to the list of reg values for the kegg_id
                    kegg_reg_dict[kegg_id].append(reg)
    else:    # if it does not match organism, use old functionality
        gene_uniprot_dict = convert_gene_symbols_to_uniprot_mygene(gene_reg_dict.keys(), organism=organism)

        uniprot_reg_dict = {}
        for gene, uniprot in gene_uniprot_dict.items():
            if isinstance(uniprot, list):
                print(f"Multiple UniProt IDs found for {gene}.")
                # Join the UniProt IDs into a single string separated by ", "
                uni_ids_str = ", ".join(uniprot)
                for uni in uniprot:
                    uniprot_reg_dict[uni] = gene_reg_dict[gene]
                # Print the gene mapping to the joined string of UniProt IDs
                print(f"Mapping {gene} to {uni_ids_str}.")
            else:
                uniprot_reg_dict[uniprot] = gene_reg_dict[gene]

        kegg_uniprots_dict = uniprot_to_kegg_dict(uniprot_reg_dict.keys())

        kegg_reg_dict = {k: [uniprot_reg_dict[uni] for uni in v if uni in uniprot_reg_dict] for k, v in
                         kegg_uniprots_dict.items()}

    annotate_genes_on_pathway(pathway_id, kegg_reg_dict, plot_dir=plot_dir, transparency=transparency, community=community, show=show, background=background, suffix=suffix)

def create_non_linear_colormap(non_linear_region = 0.0005, intensity_limit=0.25):
    """
    Creates a non-linear colormap that mimics 'coolwarm' with adjustments.

    Parameters:
    - intensity_limit: Adjusts the steepness of the slope around ±0.01.

    Returns:
    - A matplotlib colormap instance.
    """

    # Define the non-linear transformation centered at 0
    def non_linear_transform(val, non_linear_region):
        non_linear_region = non_linear_region
        if abs(val) < non_linear_region:
            return 0.5 * intensity_limit * (val / non_linear_region) + 0.5
        else:
            return (0.5 - intensity_limit) * (abs(val) - non_linear_region) / (0.5 - non_linear_region) * np.sign(
                val) + 0.5 + intensity_limit * np.sign(val)

    # Create the 'coolwarm' colormap
    coolwarm = plt.get_cmap('coolwarm')

    # Normalize the input for the colormap definition
    def normalize(value, start, end):
        return (value - start) / (end - start)

    # Generate a custom colormap by applying the non-linear transformation
    cdict = {'red': [], 'green': [], 'blue': []}
    # Ensure the loop runs from 0 to 1
    for x in np.linspace(0, 1, 256):  # Corrected normalization
        # Apply transformation within normalized -1 to 1 space, then adjust for colormap
        transformed_x = non_linear_transform(x * 2 - 1, non_linear_region)  # Adjust to -1 to 1 space
        r, g, b, _ = coolwarm(transformed_x)
        cdict['red'].append((x, r, r))
        cdict['green'].append((x, g, g))
        cdict['blue'].append((x, b, b))

    # Create and return the non-linear colormap
    return LinearSegmentedColormap('Custom_Coolwarm', segmentdata=cdict, N=256)

def annotate_genes_on_pathway(pathway_id, kegg_reg_dict, plot_dir=".", transparency=.5, community=None, show=True, background='transparent', suffix=''):

    # ensure dir existence
    pathlib.Path(plot_dir + "/KEGG/").mkdir(parents=True, exist_ok=True)
    if community is not None:
        pathlib.Path(plot_dir + "/KEGG/" + str(community) + "/").mkdir(parents=True, exist_ok=True)

    # Fetch the KGML content to get information about KEGG IDs
    kgml_content = fetch_pathway_kgml(pathway_id)
    graphics_info = parse_kegg_ids_from_kgml_v2(kgml_content)

    # Download the pathway image
    match = re.search(r"\d", pathway_id)
    if match:
        index = match.start()
        organism_code = pathway_id[:index]
        image_url = f"https://www.kegg.jp/kegg/pathway/{organism_code}/{pathway_id}.png"
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
    else:
        raise AttributeError("Invalid pathway ID format.")

    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Define color map and normalization
    min_expr = min(min(values) for values in kegg_reg_dict.values())
    max_expr = max(max(values) for values in kegg_reg_dict.values())
    # Adjust min_expr and max_expr to be le/ge than 0
    min_expr = min(min_expr, -1)
    max_expr = max(max_expr, +1)

    # Create the custom colormap and normalization
    cmap = create_non_linear_colormap()
    norm = mcolors.TwoSlopeNorm(vmin=min_expr, vcenter=0, vmax=max_expr)

    for graphic_id, (positional_info, kegg_ids) in graphics_info.items():
        x, y, w, h = positional_info['x'], positional_info['y'], positional_info['width'], positional_info['height']

        # Collect all regulations associated with the KEGG IDs of this graphic object
        all_regulations = [kegg_reg_dict[kegg_id] for kegg_id in kegg_ids if kegg_id in kegg_reg_dict]

        # Flatten the list of lists into a single list of regulations
        regulations = sorted([reg for sublist in all_regulations for reg in sublist])

        num_regs = len(regulations)
        part_width = w / max(num_regs, 1)

        for i, reg in enumerate(regulations):
            color_value = cmap(norm(reg))
            color = tuple(int(255 * c) for c in color_value[:3]) + (
            int(255 * transparency),)  # Modify the alpha value as needed
            part_x = x - w / 2 + part_width * i
            draw.rectangle([part_x, y - h / 2, part_x + part_width, y + h / 2], fill=color)

    # Blend the overlay with the original image
    img_with_overlay = Image.alpha_composite(img, overlay)

    # Create a new ImageDraw object for img_with_overlay
    draw_overlay = ImageDraw.Draw(img_with_overlay)

    # Then proceed with your legend drawing code, but use draw_overlay instead of draw
    # Parameters for the legend remain the same
    legend_width = 100  # Width of the legend
    legend_height = 20  # Height of the legend
    margin = 10  # Margin from the top and right edges
    text_offset = 10  # Offset for the text below the legend

    # Calculate legend position
    legend_top = margin*1.5
    legend_right = img_with_overlay.width - margin*2

    # Create a gradient legend on img_with_overlay
    for i in range(legend_width):
        ratio = i / legend_width
        color_value = cmap(ratio)
        color = tuple(int(255 * c) for c in color_value[:3]) + (255,)  # Full opacity
        draw_overlay.rectangle([legend_right - legend_width + i, legend_top,
                                legend_right - legend_width + i + 1, legend_top + legend_height], fill=color)

    # Text annotations for vmin, vcenter, and vmax, using draw_overlay
    draw_overlay.text((legend_right - legend_width, legend_top + legend_height + text_offset), f"{min_expr:.1f}",
                      fill="black")
    draw_overlay.text((legend_right - legend_width / 2, legend_top + legend_height + text_offset), "0", fill="black")
    # Before drawing the text, calculate the text width
    max_expr_text = f"{max_expr:.1f}"
    text_width = draw_overlay.textlength(max_expr_text)
    draw_overlay.text((legend_right - text_width, legend_top + legend_height + text_offset), max_expr_text,
                      fill="black")

    # Continue to display or save img_with_overlay as before
    plt.figure(figsize=(20, 20))
    plt.imshow(img_with_overlay)
    plt.axis('off')

    change_background_color(plt.gcf(), plt.gca(), background)

    if community is not None:  # if specified
        file_name = plot_dir + '/KEGG/' + str(community) + '/' + pathway_id + suffix + '.png'
    else:  # if unspecified
        file_name = plot_dir + "/KEGG/" + pathway_id + suffix + '.png'

    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    print("Saving KEGG pathways to %s" %file_name)
    if show:
        plt.show()
    plt.close()

def fetch_pathway_kgml(pathway_id):
    url = f"http://rest.kegg.jp/get/{pathway_id}/kgml"
    response = requests.get(url)
    if response.ok:
        return response.content  # Returns the content of the KGML file
    else:
        print(f"Failed to fetch KGML for pathway {pathway_id}")
        return None

def parse_kegg_ids_from_kgml_v2(kgml_content):
    root = ET.fromstring(kgml_content)
    graphics_dict = {}
    for entry in root.findall(".//entry[@type='gene']"):
        entry_id = entry.get('id')  # Unique identifier for each graphic object
        graphics = entry.find('.//graphics')
        if graphics is not None:
            # Extracting positional information
            x = int(graphics.attrib.get('x', 0))
            y = int(graphics.attrib.get('y', 0))
            width = int(graphics.attrib.get('width', 0))
            height = int(graphics.attrib.get('height', 0))
            positional_info = {'x': x, 'y': y, 'width': width, 'height': height}

            # Extracting KEGG IDs associated with this graphic object
            entry_names = entry.get('name', '').split()

            # Creating the dictionary entry
            graphics_dict[entry_id] = (positional_info, entry_names)
    return graphics_dict

def convert_gene_symbols_to_uniprot_mygene(gene_symbols, organism='9606'):
    base_url = "https://mygene.info/v3/query"
    gene_to_uniprot = {}  # Dictionary to store gene symbol to UniProt ID mappings
    for gene_symbol in gene_symbols:
        params = {
            'q': gene_symbol,
            'scopes': 'symbol',
            'fields': 'uniprot',
            'species': organism
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'hits' in data and len(data['hits']) > 0:
                # Extracting UniProt ID from the first hit
                hit = data['hits'][0]
                if 'uniprot' in hit and 'Swiss-Prot' in hit['uniprot']:
                    gene_to_uniprot[gene_symbol] = hit['uniprot']['Swiss-Prot']
                elif 'uniprot' in hit and 'TrEMBL' in hit['uniprot']:
                    gene_to_uniprot[gene_symbol] = hit['uniprot']['TrEMBL']
                else:
                    gene_to_uniprot[gene_symbol] = None
                    print(f"No UniProt ID found for the gene symbol: {gene_symbol}.")
            else:
                gene_to_uniprot[gene_symbol] = None
                print(f"No UniProt ID found for the gene symbol: {gene_symbol}.")
        else:
            print(f"Failed to fetch data from MyGene.info API for {gene_symbol}. Status code: {response.status_code}")
            print(hit)
            gene_to_uniprot[gene_symbol] = None
    return gene_to_uniprot

def uniprot_to_kegg_dict(uniprot_ids):
    kegg_to_uniprots = {}  # Dictionary to store KEGG ID to UniProt IDs mappings
    for uniprot_id in uniprot_ids:
        url = f"http://rest.kegg.jp/conv/genes/uniprot:{uniprot_id}"
        response = requests.get(url)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                parts = line.split('\t')
                if len(parts) == 2:
                    kegg_id = parts[1]  # Extracting KEGG ID
                    if kegg_id not in kegg_to_uniprots:
                        kegg_to_uniprots[kegg_id] = [uniprot_id]
                    else:
                        kegg_to_uniprots[kegg_id].append(uniprot_id)
        else:
            print(f"Failed to fetch data for UniProt ID {uniprot_id}. Status code: {response.status_code}")
    return kegg_to_uniprots

def scale_parameters_based_on_network_size(G, base_font_size=8, base_fig_size=12):
    """
    Adjust node size, font size, and edge width based on the number of nodes in the graph.

    :param G: The graph for which to scale parameters.
    :param base_node_size: Base node size to scale from.
    :param base_font_size: Base font size to scale from.
    :param base_edge_width: Base edge width to scale from.
    :return: Tuple of (node_size, font_size, edge_width) after scaling.
    """
    num_nodes = len(G.nodes)

    # Define scaling factors - these values are adjustable based on desired appearance
    if num_nodes < 50:
        scale_factor = 0.85
    elif num_nodes < 100:
        scale_factor = 0.75
    elif num_nodes < 150:
        scale_factor = 0.55
    elif num_nodes < 250:
        scale_factor = 0.35
    else:
        scale_factor = 0.25

    font_size = base_font_size / scale_factor
    fig_size = base_fig_size / scale_factor

    return font_size, fig_size

def plotRegNetworks(G, partition, centrality, plot_dir=".", full_network=False, centrality_measure = 'w_degree', community='all', show=True, background='transparent', min_comm_size=3):

    # ensure dir existence
    pathlib.Path(plot_dir + "/regNetworks/").mkdir(parents=True, exist_ok=True)

    if full_network: #community parameter ignored here
        # Create a colormap for the nodes based on their 'regulation' attribute
        cmap = plt.cm.coolwarm

        # Adjust vmin and vmax for specific community
        nodes = G.nodes
        regulations = [G.nodes[node]['regulation'] for node in nodes]
        vmin = min(regulations) if min(regulations) < -1 else -1
        vmax = max(regulations) if max(regulations) > 1 else 1
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

        # Create the original greyscale colormap for edges
        cmap_grey = plt.cm.Greys
        dark_grey_cmap = mpl.colors.LinearSegmentedColormap.from_list(
            "dark_grey", cmap_grey(np.linspace(0.3, 1, 256))
        )

        # Calculate the layout of the graph
        pos = nx.kamada_kawai_layout(G)

        # Calculate dynamic sizes
        font_size_legend, fig_size = scale_parameters_based_on_network_size(G)

        # Prepare figure
        plt.figure(figsize=(fig_size, fig_size))
        plt.title(f'Network Visualization for Full Network', fontdict={'fontsize': font_size_legend})

        # Node colors and sizes based on 'regulation' attribute
        node_colors = [cmap(norm(G.nodes[node]['regulation'])) for node in G.nodes]

        # Normalize edge weights for width and alpha
        edge_weights_raw = np.array([G.edges[edge]['weight'] for edge in G.edges])
        edge_weights = edge_weights_raw * 4  # Now scaling with dynamic edge width
        edge_alphas = np.interp(edge_weights_raw, (edge_weights_raw.min(), edge_weights_raw.max()), (0.1, 1))

        if centrality_measure:
            # Check if centrality_measure is valid
            if not any(centrality_measure in measures for measures in centrality['Full Network'].values()):
                raise AttributeError(
                    f"Invalid centrality measure. Choose from {', '.join({key for measures in centrality['Full Network'].values() for key in measures})}")

            centrality_values = {gene: measures[centrality_measure] for gene, measures in
                                 centrality['Full Network'].items() if centrality_measure in measures}

            # Normalize centrality values for visualization
            max_centrality = max(centrality_values.values())
            normalized_centrality = {node: 1000 + centrality / max_centrality * 1500 for node, centrality in
                                     centrality_values.items()}

            # Use normalized centrality for node size
            node_sizes = [normalized_centrality[node] for node in G.nodes]
        else:
            node_sizes = [2000 for node in G.nodes]

        # Custom function to draw halos
        def draw_halos(pos, node_sizes, node_alphas, ax):
            for node, size in node_sizes.items():
                alpha = node_alphas[node]
                nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=size * 1.5, node_color='yellow',
                                       alpha=alpha, ax=ax)

        # Draw color reference rectangle in the upper right corner
        ax = plt.gca()

        # Draw halos
        node_alphas = {node: centrality / max(centrality_values.values()) for node, centrality in
                       centrality_values.items()}
        draw_halos(pos, normalized_centrality, node_alphas, ax)

        # Draw the network
        nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color=edge_alphas, edge_cmap=dark_grey_cmap,
                               alpha=0.5)
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=cmap)

        # Custom method to draw labels with outlines for readability
        for node, (x, y) in pos.items():
            text = node
            plt.text(x, y, text, fontsize=8, ha='center', va='center',
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha=0.5))

        # Create a colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        # After creating the colorbar
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.046 * 0.6, pad=0.04)
        cbar.set_label('Regulation', fontsize=font_size_legend)  # Adjust the font size for the label here
        cbar.ax.invert_yaxis()

        # Function to plot legend nodes next to the colorbar
        def plot_legend_node_near_colorbar(node, centrality_value, position):
            node_color = cmap(norm(G.nodes[node]['regulation']))
            node_size = normalized_centrality[node]   # Adjust size scaling as needed for visibility
            halo_size = node_size * 1.5  # Make the halo slightly larger than the node

            # Calculate positions relative to the colorbar
            if position == 'above':
                x, y = 1.05, 0.9  # Adjust these coordinates as needed
            elif position == 'below':
                x, y = 1.05, 0.1  # Adjust these coordinates as needed

            # Transform from axis to figure coordinates for the center of the halo/node
            x_fig, y_fig = ax.transAxes.transform((x, y))  # This gets you axis -> display coords
            inv = plt.gcf().transFigure.inverted()
            x_fig, y_fig = inv.transform((x_fig, y_fig))  # Convert display coords -> figure coords

            # Adjust ax_fig size to fit both halo and node
            ax_fig = plt.gcf().add_axes([x_fig, y_fig, 0.05, 0.05], anchor='C', zorder=1)
            ax_fig.axis('off')

            # Draw the halo
            ax_fig.scatter(0.5, 0.5, s=halo_size, color='yellow', alpha=node_alphas[node],  zorder=1)

            # Draw the node on top of the halo
            ax_fig.scatter(0.5, 0.5, s=node_size, color=node_color, edgecolor='black', zorder=2)

            ax_fig.set_xlim(0, 1)
            ax_fig.set_ylim(0, 1)
            ax_fig.axis('off')


            # Node name
            ax_fig.text(0.5, -0.2, f"{node}\n\n", ha='center', va='center', fontsize=font_size_legend,
                        transform=ax_fig.transAxes)

            # Centrality measure (smaller font size)
            measure_text = "\nWeighted " if centrality_measure.startswith('w_') else "\n"
            measure_text += f"{centrality_measure.replace('w_', '').capitalize()} Centrality\n"
            ax_fig.text(0.5, -0.2, measure_text, ha='center', va='center',
                        fontsize=font_size_legend-2, transform=ax_fig.transAxes)

            # Centrality value (original font size)
            ax_fig.text(0.5, -0.2, f"\n\n{centrality_value:.2f}", ha='center', va='center',
                        fontsize=font_size_legend, transform=ax_fig.transAxes)



        if centrality_measure:
            # Identify min and max centrality nodes
            min_node = min(centrality_values, key=centrality_values.get)
            max_node = max(centrality_values, key=centrality_values.get)

            # Plot the min and max centrality nodes near the colorbar
            plot_legend_node_near_colorbar(max_node, centrality_values[max_node], 'above')
            plot_legend_node_near_colorbar(min_node, centrality_values[min_node], 'below')

        plt.axis('off')
        file_name = plot_dir + '/regNetworks/fullNetwork.png'

        change_background_color(plt.gcf(), plt.gca(), background)

        plt.savefig(file_name, dpi=300, bbox_inches='tight')
        print("Saving regulatory network to %s" % file_name)
        if show == True:
            plt.show()
        plt.close()

    else:

        if community == 'all':
            communities = set(partition.values())
            all_regulations = [G.nodes[node]['regulation'] for node in G.nodes]
            vmin = min(all_regulations) if min(all_regulations) < -1 else -1
            vmax = max(all_regulations) if max(all_regulations) > 1 else 1
        else:
            communities = [community]

        for comm in communities:

            # Create a colormap for the nodes based on their 'regulation' attribute
            cmap = plt.cm.coolwarm
            if community != 'all':
                # Adjust vmin and vmax for specific community
                nodes_in_community = [node for node, c in partition.items() if c == comm]
                regulations = [G.nodes[node]['regulation'] for node in nodes_in_community]
                vmin = min(regulations) if min(regulations) < -1 else -1
                vmax = max(regulations) if max(regulations) > 1 else 1
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

            # Create the original greyscale colormap for edges
            cmap_grey = plt.cm.Greys
            dark_grey_cmap = mpl.colors.LinearSegmentedColormap.from_list(
                "dark_grey", cmap_grey(np.linspace(0.3, 1, 256))
            )

            # Filter nodes by community using the partition dictionary
            nodes_in_community = [node for node, c in partition.items() if c == comm]
            if len(nodes_in_community) < min_comm_size:
                continue
            G_sub = G.subgraph(nodes_in_community)

            # Calculate the layout of the graph
            pos = nx.kamada_kawai_layout(G_sub)

            # Calculate dynamic sizes
            font_size_legend, fig_size = scale_parameters_based_on_network_size(G)

            # Prepare figure
            plt.figure(figsize=(fig_size, fig_size))
            plt.title(f'Network Visualization for Community {comm}', fontdict={'fontsize': font_size_legend})

            # Node colors and sizes based on 'regulation' attribute
            node_colors = [cmap(norm(G_sub.nodes[node]['regulation'])) for node in G_sub.nodes]

            # Normalize edge weights for width and alpha
            edge_weights_raw = np.array([G_sub.edges[edge]['weight'] for edge in G_sub.edges])
            edge_weights = edge_weights_raw * 4  # Adjust scaling as necessary
            edge_alphas = np.interp(edge_weights_raw, (edge_weights_raw.min(), edge_weights_raw.max()), (0.1, 1))

            if centrality_measure:
                # Check if centrality_measure is valid
                if not any(centrality_measure in measures for measures in centrality[comm].values()):
                    raise AttributeError(
                        f"Invalid centrality measure. Choose from {', '.join({key for measures in centrality[comm].values() for key in measures})}")

                centrality_values = {gene: measures[centrality_measure] for gene, measures in
                                     centrality[comm].items() if centrality_measure in measures}

                # Normalize centrality values for visualization
                max_centrality = max(centrality_values.values())
                normalized_centrality = {node: 1000 + centrality / max_centrality * 1500 for node, centrality in
                                         centrality_values.items()}

                # Use normalized centrality for node size
                node_sizes = [normalized_centrality[node] for node in G_sub.nodes]
            else:
                node_sizes = [2000 for node in G_sub.nodes]

            # Custom function to draw halos
            def draw_halos(pos, node_sizes, node_alphas, ax):
                for node, size in node_sizes.items():
                    alpha = node_alphas[node]
                    nx.draw_networkx_nodes(G_sub, pos, nodelist=[node], node_size=size * 1.5, node_color='yellow',
                                           alpha=alpha, ax=ax)

            # Draw color reference rectangle in the upper right corner
            ax = plt.gca()

            # Draw halos
            node_alphas = {node: centrality / max(centrality_values.values()) for node, centrality in
                           centrality_values.items()}
            draw_halos(pos, normalized_centrality, node_alphas, ax)

            # Draw the network
            nx.draw_networkx_edges(G_sub, pos, width=edge_weights, edge_color=edge_alphas, edge_cmap=dark_grey_cmap, alpha=0.5)
            nx.draw_networkx_nodes(G_sub, pos, node_size=node_sizes, node_color=node_colors, cmap=cmap)

            # Custom method to draw labels with outlines for readability
            for node, (x, y) in pos.items():
                text = node
                plt.text(x, y, text, fontsize=8, ha='center', va='center',
                         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha=0.5))

            # Create a colorbar as a legend
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            # After creating the colorbar
            cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.046 * 0.6, pad=0.04)
            cbar.set_label('Regulation', fontsize=font_size_legend)  # Adjust the font size for the label here
            cbar.ax.invert_yaxis()

            # Function to plot legend nodes next to the colorbar
            def plot_legend_node_near_colorbar(node, centrality_value, position):
                node_color = cmap(norm(G_sub.nodes[node]['regulation']))
                node_size = normalized_centrality[node]  # Adjust size scaling as needed for visibility
                halo_size = node_size * 1.5  # Make the halo slightly larger than the node
                node_label = f"{node}\n{centrality_measure.capitalize()} {centrality_value:.2f}"

                # Calculate positions relative to the colorbar
                if position == 'above':
                    x, y = 1.05, 0.9  # Adjust these coordinates as needed
                elif position == 'below':
                    x, y = 1.05, 0.1  # Adjust these coordinates as needed

                # Transform from axis to figure coordinates for the center of the halo/node
                x_fig, y_fig = ax.transAxes.transform((x, y))  # This gets you axis -> display coords
                inv = plt.gcf().transFigure.inverted()
                x_fig, y_fig = inv.transform((x_fig, y_fig))  # Convert display coords -> figure coords

                # Adjust ax_fig size to fit both halo and node
                ax_fig = plt.gcf().add_axes([x_fig, y_fig, 0.05, 0.05], anchor='C', zorder=1)
                ax_fig.axis('off')

                # Draw the halo
                ax_fig.scatter(0.5, 0.5, s=halo_size, color='yellow', alpha=node_alphas[node], zorder=1)

                # Draw the node on top of the halo
                ax_fig.scatter(0.5, 0.5, s=node_size, color=node_color, edgecolor='black', zorder=2)

                ax_fig.set_xlim(0, 1)
                ax_fig.set_ylim(0, 1)
                ax_fig.axis('off')

                # Node name
                ax_fig.text(0.5, -0.2, f"{node}\n\n", ha='center', va='center', fontsize=font_size_legend,
                            transform=ax_fig.transAxes)

                # Centrality measure (smaller font size)
                measure_text = "\nWeighted " if centrality_measure.startswith('w_') else "\n"
                measure_text += f"{centrality_measure.replace('w_', '').capitalize()} Centrality\n"
                ax_fig.text(0.5, -0.2, measure_text, ha='center', va='center',
                            fontsize=font_size_legend - 2, transform=ax_fig.transAxes)

                # Centrality value (original font size)
                ax_fig.text(0.5, -0.2, f"\n\n{centrality_value:.2f}", ha='center', va='center',
                            fontsize=font_size_legend, transform=ax_fig.transAxes)

            if centrality_measure:

                # Identify min and max centrality nodes
                min_node = min(centrality_values, key=centrality_values.get)
                max_node = max(centrality_values, key=centrality_values.get)

                # Plot the min and max centrality nodes near the colorbar
                plot_legend_node_near_colorbar(max_node, centrality_values[max_node], 'above')
                plot_legend_node_near_colorbar(min_node, centrality_values[min_node], 'below')

            plt.axis('off')
            file_name = plot_dir + '/regNetworks/community_' + str(comm) + '.png'

            change_background_color(plt.gcf(), plt.gca(), background)

            # Continue with saving or showing the figure
            plt.savefig(file_name, dpi=300, bbox_inches='tight')
            print("Saving regulatory networks to %s" % file_name)
            if show == True:
                plt.show()
            plt.close()

def visualize_Reactome(pathway_id, gene_reg_dict, organism=9606, plot_dir=".", community=None, background='transparent', show=True, suffix=''):

    # ensure dir existence
    pathlib.Path(plot_dir + "/Reactome/").mkdir(parents=True, exist_ok=True)
    if community is not None:
        pathlib.Path(plot_dir + "/Reactome/" + str(community) + "/").mkdir(parents=True, exist_ok=True)

    if organism == 'human':
        organism = 9606
    elif organism == 'mouse':
        organism = 10090

    # Fetch the pathway image
    pathway_image_data = fetch_reactome_pathway_image(pathway_id=pathway_id, gene_reg_dict=gene_reg_dict, organism=organism, image_format='PNG')

    if community is not None:  # if specified
        file_name = plot_dir + '/Reactome/' + str(community) + '/' + pathway_id + suffix + '.png'
    else:  # if unspecified
        file_name = plot_dir + "/Reactome/" + pathway_id + suffix + '.png'

    with open(file_name, 'wb') as file:
        file.write(pathway_image_data)

    print(f"Image saved to {file_name}")

    if show:
        print(pathway_id)
        from IPython.display import Image, display
        display(Image(pathway_image_data))

def fetch_reactome_pathway_image(gene_reg_dict, pathway_id, organism, image_format, interactors=False):
    # Step 1: Post gene expressions to get the analysis token
    analysis_url = f'https://reactome.org/AnalysisService/identifiers/?interactors=false&species={organism}&pageSize=20&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL&pValue=1&includeDisease=true'
    gene_data = '\n'.join([f'{gene}, {exp}' for gene, exp in gene_reg_dict.items()])
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.post(analysis_url, headers=headers, data=gene_data)
    if response.status_code != 200:
        raise ValueError(f"Failed to post gene expressions. Status code: {response.status_code}")
    analysis_token = response.json()['summary']['token']

    # Step 2: Fetch the pathway diagram image using the token
    image_url = f'https://reactome.org/ContentService/exporter/diagram/{pathway_id}.{image_format}?quality=10&flgInteractors={interactors}&title=true&margin=15&ehld=true&diagramProfile=Modern&token={analysis_token}&resource=TOTAL&analysisProfile=Strosobar%2C%20Copper%2520Plus'

    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        print(analysis_token)
        print(pathway_id)
        raise ValueError(f"Failed to fetch pathway image. Status code: {image_response.status_code}")

    # Return the image data for display
    return image_response.content

def visualize_wikipathway(pathway_id, gene_reg_dict, plot_dir=".", community=None, show=True, suffix=''):

    pathway_path = download_wikipathway_svg(pathway_id, plot_dir=plot_dir, community=community, suffix=suffix)

    draw_on_pathway(pathway_path, gene_reg_dict)

    def display_image_html(image_path):
        from IPython.display import display, HTML

        image_html = f'<img src="{image_path}" alt="Image">'
        display(HTML(image_html))

    if show:
        print(pathway_id)
        display_image_html(pathway_path)

def download_wikipathway_svg(pathway_id, plot_dir='.', community=None, suffix=''):

    # ensure dir existence
    pathlib.Path(plot_dir + "/WikiPathways/").mkdir(parents=True, exist_ok=True)
    if community is not None:
        pathlib.Path(plot_dir + "/WikiPathways/" + str(community) + "/").mkdir(parents=True, exist_ok=True)


    # Download the PNG image
    svg_url = f"https://www.wikipathways.org/wikipathways-assets/pathways/{pathway_id}/{pathway_id}.svg"
    response = requests.get(svg_url)

    if community is not None:  # if specified
        file_name = plot_dir + '/WikiPathways/' + str(community) + '/' + pathway_id + suffix + '.svg'
    else:  # if unspecified
        file_name = plot_dir + "/WikiPathways/" + pathway_id + suffix + '.svg'

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {file_name}")
    else:
        print(f"Failed to download SVG. Status code: {response.status_code}")

    return file_name

def draw_on_pathway(pathway_path, gene_reg_dict):
    # Load and parse the SVG file
    tree = ET.parse(pathway_path)
    root = tree.getroot()

    # Iterate through each gene in the regulation dictionary
    for gene, regulation in gene_reg_dict.items():
        # Attempt to find all <a> elements, then filter them
        for elem in root.findall('.//{http://www.w3.org/2000/svg}a'):
            # Check if the 'class' attribute contains the gene name
            elem_class = elem.get('class', '')
            if f'HGNC_{gene}' in elem_class.split():
                # Find the <rect> element to change its color
                rect = elem.find('.//{http://www.w3.org/2000/svg}rect')
                if rect is not None:
                    # Set the fill color based on the gene's regulation value
                    color = '#ff0000' if regulation > 0 else '#0000ff'
                    rect.set('style', f'fill:{color};fill-opacity:0.5')

    # Save the modified SVG file
    tree.write(pathway_path)

