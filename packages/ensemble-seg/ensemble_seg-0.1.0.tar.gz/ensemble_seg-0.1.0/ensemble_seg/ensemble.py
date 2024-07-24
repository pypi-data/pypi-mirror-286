import numpy as np
import numba as nb
import cv2

from typing import Iterator


# calculate the IOU between two masks
@nb.njit
def mask_iou(mask1, mask2):
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    return intersection / union


@nb.njit
def bbox_iou(bbox1, bbox2):
    x1, y1, x2, y2 = bbox1
    x3, y3, x4, y4 = bbox2
    
    x5 = max(x1, x3)
    y5 = max(y1, y3)
    x6 = min(x2, x4)
    y6 = min(y2, y4)
    
    intersection = max(0, x6 - x5) * max(0, y6 - y5)
    union = (x2 - x1) * (y2 - y1) + (x4 - x3) * (y4 - y3) - intersection
    
    return intersection / union


@nb.njit
def get_overlap_graph(
    instances: list[dict],
    iou_threshold: float = 0.8,
    area_diff_percent: float = 0.1,
    iou_method: str = 'mask',
    area_method: str = 'mask',
) -> dict:
    """
    Given a list of instances, returns a graph where each node is an instance and 
    each edge is an overlap between instances.
    
    Args:
        instances (list[dict]): the list of instances to compare
        iou_threshold (float, optional): threshold of IOU. Defaults to 0.8.
        area_diff_percent (float, optional): percent of different between areas. Defaults to 0.1.
        iou_method (str, optional): method to compare IOU's. Defaults to 'mask'.
        area_method (str, optional): method to compare areas. Defaults to 'mask'.

    Raises:
        ValueError: When iou_method or area_method are not 'mask' or 'bbox'

    Returns:
        dict: a graph where each node is an instance and each edge is an overlap between instances
    """
    graph = {}

    for i, in1 in enumerate(instances):
        graph[i] = []

        for j, in2 in enumerate(instances):
            if i == j:
                continue

            iou = None
            areas_are_close = False

            if iou_method == 'mask':
                iou = mask_iou(in1['mask'], in2['mask'])

            elif iou_method == 'bbox':
                iou = bbox_iou(in1['bbox'], in2['bbox'])

            else:
                raise ValueError(f"Unknown iou method: {iou_method}. Must be 'mask' or 'bbox'")

            if area_method == 'mask':
                area1 = in1['mask'].sum()
                area2 = in2['mask'].sum()
                area_diff = abs(area1 - area2)
                areas_are_close = area_diff < area_diff_percent * min(area1, area2)

            elif area_method == 'bbox':
                area1 = (in1['bbox'][2] - in1['bbox'][0]) * (in1['bbox'][3] - in1['bbox'][1])
                area2 = (in2['bbox'][2] - in2['bbox'][0]) * (in2['bbox'][3] - in2['bbox'][1])
                area_diff = abs(area1 - area2)
                areas_are_close = area_diff < area_diff_percent * min(area1, area2)

            else:
                raise ValueError(f"Unknown area method: {area_method}. Must be 'mask' or 'bbox'")

            if iou > iou_threshold and areas_are_close:
                graph[i].append(j)

    return graph


@nb.njit
def merge_overlaps(graph: dict) -> set[tuple]:
    """
    Using an adjacency list graph object, groups all overlapping nodes and edges. Example:
    
    ```
        graph = {0: [], 1: [0], 2: [], 3: [0, 1], 4: [2]}
        overlaps = [(0, 1, 3), (2, 4)]
    ```
    
    Args:
        graph (dict): an adjacency list graph object where each key is a node and each value is a list of edges
    
    Returns:
        set[tuple]: a set of tuples where each tuple is a group of overlapping nodes and edges
    """
    grouped = set()
    
    for i in graph:

        if len(graph[i]) == 0:
            continue

        visited = set()
        visited.add(i)
        visited.update(graph[i])

        for j in graph:
            if i == j:
                continue

            # if any visited are in g[j], add all edges to visited
            if any([k in visited for k in graph[j]]):
                visited.update(graph[j])
                visited.add(j)

        if len(visited) > 0:
            grouped.add(tuple(sorted(visited)))
            
    return grouped


def blend_masks(masks: list[np.ndarray], blur_kernel=(21, 21)) -> np.ndarray:
    """Given a list of masks, blends them together with equal weight into a single mask.

    Args:
        masks (list[np.ndarray]): a list of masks to blend
        blur_kernel (tuple[int], optional): kernel to use when bluring masks together. Defaults to (21, 21).

    Returns:
        np.ndarray: a single blended binary mask
    """
    blended = np.zeros_like(masks[0])
    blended = cv2.cvtColor(blended, cv2.COLOR_GRAY2BGR)

    for mask in masks:
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        blended = cv2.addWeighted(blended, 1, mask, 0.5, 0)

    # add small blur to smooth out the edges
    blended = cv2.blur(blended, blur_kernel)
    
    blended = cv2.cvtColor(blended, cv2.COLOR_BGR2GRAY)
    
    # threshold at 50% to get a binary mask
    _, blended = cv2.threshold(blended, 127, 255, cv2.THRESH_BINARY)

    return blended


def merge_masks(
    instances: list[dict],
    iou_threshold: float = 0.8,
    area_diff_percent: float = 0.1,
    iou_method: str = 'mask',
    area_method: str = 'mask',
) -> Iterator[tuple[list[int], np.ndarray]]:
    """Merges overlapping instances into a single instance with a blended mask.

    Args:
        instances (list[dict]): a list of instances to merge. Each dict should be in the format:
            {
                'mask': np.ndarray, # binary mask
                'bbox': tuple[int], # bounding box (x1, y1, x2, y2)
            }

        iou_threshold (float, optional): threshold of IOU. Defaults to 0.8.
        area_diff_percent (float, optional): percent of different between areas. Defaults to 0.1.
        iou_method (str, optional): method to compare IOU's. Defaults to 'mask'.
        area_method (str, optional): method to compare areas. Defaults to 'mask'.

    Yields:
        Iterator[tuple[list[int], np.ndarray]]: the list of instance indices that were merged and the blended mask
    """
    
    graph = get_overlap_graph(
        instances,
        iou_threshold=iou_threshold,
        area_diff_percent=area_diff_percent,
        iou_method=iou_method,
        area_method=area_method
    )
    
    grouped = merge_overlaps(graph)
    
    for group in grouped:        
        masks = []

        for i in group:
            mask = instances[i]['mask']
            # ensure mask is binary
            mask[mask > 0] = 255
            masks.append(mask)
            
        blended = blend_masks(masks)
        
        yield group, blended