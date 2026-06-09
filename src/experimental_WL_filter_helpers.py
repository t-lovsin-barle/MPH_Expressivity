from ast import For
import os

from collections import Counter, defaultdict

import numpy as np
import networkx as nx
import math

# ── multipers runtime patch ──────────────────────────────────────────────
import multipers as mp
import multipers.filtrations as mpf
import multipers.array_api.numpy as _mp_np_api


def _patched_device(x):
    return "cpu" if isinstance(x, np.ndarray) else x.device

def _patched_to_device(x, device):
    return x if isinstance(x, np.ndarray) else x.to_device(device)




_mp_np_api.device    = _patched_device
_mp_np_api.to_device = _patched_to_device


def convert_labels_to_colors(raw_labels):
    """Map raw aggregated strings → compact integer color IDs."""
    unique = sorted(set(raw_labels))
    mapping = {label: idx for idx, label in enumerate(unique)}
    return [mapping[l] for l in raw_labels]

def neighbour_labels_aggregation(G, node, labels):
    neighbour_lbls = sorted(str(labels[nbr]) for nbr in G.neighbors(node))
    return str(labels[node]) + "|" + ",".join(neighbour_lbls)

def compute_wl_labels(G, labels=None, max_iterations: int = 3, stable_labels: bool = False):
    if labels is None:
        labels = []
        for v in G.nodes():
            labels.append(str(G.degree(v)))

    if stable_labels:
        max_iterations = len(labels)
    prev_labels = None
    colors = convert_labels_to_colors(labels)
    for _ in range(max_iterations):
        new_labels= []
        

        for v in G.nodes():
            new_labels.append(neighbour_labels_aggregation(G, v, labels))
        
        new_colors = convert_labels_to_colors(new_labels)

        if new_colors == colors: 
            break
        colors = new_colors
        prev_labels = labels
        labels = new_labels

    if prev_labels == None:
        prev_labels = labels

    return labels, prev_labels

def label_to_counter(label_str):
    # Split off the node's own label, then split neighbours by comma
    parts = label_str.split("|")
    all_values = [parts[0]]
    for i in range(1,len(parts)):

        all_values += parts[i].split(",")
    return Counter(all_values)



def l1_distance(c1, c2):
    all_keys = set(c1.keys()) | set(c2.keys())
    return sum(abs(c1.get(k, 0) - c2.get(k, 0)) for k in all_keys)









