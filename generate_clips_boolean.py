import os
import trimesh
import numpy as np
from trimesh.boolean import union

# clip base dimensions
clip_length = 60.0
clip_width = 25.0
clip_height = 20.0
wall_thickness = 3.0
lip_depth = 10.0
lip_height = 4.0

# cover thickness and y offset
cover_thickness = 4.39


def make_clip(gap):
    inner_height = cover_thickness + gap
    base = trimesh.creation.box(
        extents=(clip_length, clip_width, clip_height),
        transform=trimesh.transformations.translation_matrix((0, clip_width / 2.0, clip_height / 2.0)),
    )
    # hollow interior for the cover jaw
    jaw = trimesh.creation.box(
        extents=(clip_length - 2.0 * wall_thickness, clip_width - lip_depth, inner_height),
        transform=trimesh.transformations.translation_matrix((0, (clip_width - lip_depth) / 2.0 + lip_depth, inner_height / 2.0)),
    )
    # internal catch lip for support
    catch = trimesh.creation.box(
        extents=(clip_length - 2.0 * wall_thickness, wall_thickness, 1.5),
        transform=trimesh.transformations.translation_matrix((0, lip_depth - 0.75, 0.75)),
    )
    # create top cover to close top and hold strength
    top_plate = trimesh.creation.box(
        extents=(clip_length, wall_thickness, clip_height - inner_height),
        transform=trimesh.transformations.translation_matrix((0, clip_width - wall_thickness / 2.0, inner_height + (clip_height - inner_height) / 2.0)),
    )

    parts = [base, catch, top_plate]
    clip = union(parts, engine='manifold')

    # cut interior cavity
    hollow = trimesh.creation.box(
        extents=(clip_length - 2.0 * wall_thickness, clip_width - (lip_depth + wall_thickness), inner_height),
        transform=trimesh.transformations.translation_matrix((0, lip_depth + (clip_width - (lip_depth + wall_thickness)) / 2.0, inner_height / 2.0)),
    )
    if hollow.is_watertight:
        clip = clip.difference(hollow, engine='manifold')
    clip.apply_translation([0, -clip_width / 2.0, 0])
    return clip

if __name__ == '__main__':
    os.makedirs('.', exist_ok=True)
    gaps = [0.10, 0.20, 0.30]
    for gap in gaps:
        clip = make_clip(gap)
        filename = f'ps4_cover_clip_direct_gap{int(gap*100):02d}.stl'
        clip.export(filename)
        print('Exported', filename, 'faces', len(clip.faces), 'watertight', clip.is_watertight)
