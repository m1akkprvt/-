import os
import trimesh
import numpy as np

# universal clip design parameters
clip_length = 60.0  # x-axis length
clip_depth = 25.0  # y-axis depth
clip_height = 20.0  # total height
wall_thickness = 2.5
top_plate_thickness = 3.0
jaw_depth = 12.0
jaw_height = 14.0

coverage_width = 30.0  # inner cavity width

def make_clip(gap):
    # inner cavity height equals cover thickness + gap
    cover_thickness = 4.39
    inner_height = cover_thickness + gap
    # positions
    x_half = clip_length / 2.0
    y_front = 0.0
    y_back = jaw_depth
    z_bottom = 0.0
    z_top = clip_height
    top_z0 = clip_height - top_plate_thickness
    # create top plate
    top_plate = trimesh.creation.box(
        extents=(clip_length, clip_depth, top_plate_thickness),
        transform=trimesh.transformations.translation_matrix((0.0, clip_depth / 2.0, top_z0 + top_plate_thickness / 2.0)),
    )
    # left wall
    left_wall = trimesh.creation.box(
        extents=(wall_thickness, jaw_depth, clip_height - top_plate_thickness),
        transform=trimesh.transformations.translation_matrix((-(clip_length - wall_thickness) / 2.0, jaw_depth / 2.0, (clip_height - top_plate_thickness) / 2.0)),
    )
    # right wall
    right_wall = trimesh.creation.box(
        extents=(wall_thickness, jaw_depth, clip_height - top_plate_thickness),
        transform=trimesh.transformations.translation_matrix(((clip_length - wall_thickness) / 2.0, jaw_depth / 2.0, (clip_height - top_plate_thickness) / 2.0)),
    )
    # back wall
    back_wall = trimesh.creation.box(
        extents=(clip_length - 2 * wall_thickness, wall_thickness, clip_height - top_plate_thickness),
        transform=trimesh.transformations.translation_matrix((0.0, jaw_depth - wall_thickness / 2.0, (clip_height - top_plate_thickness) / 2.0)),
    )
    # inner finger to support the cover from the inside
    finger = trimesh.creation.box(
        extents=(coverage_width, wall_thickness, inner_height),
        transform=trimesh.transformations.translation_matrix((0.0, wall_thickness / 2.0, inner_height / 2.0)),
    )
    # optional ledge to catch the cover from bottom
    ledge = trimesh.creation.box(
        extents=(clip_length - 8.0, wall_thickness, 1.5),
        transform=trimesh.transformations.translation_matrix((0.0, wall_thickness + 1.0, 1.5 / 2.0)),
    )

    clip = trimesh.util.concatenate([top_plate, left_wall, right_wall, back_wall, finger, ledge])
    clip.merge_vertices()
    return clip

if __name__ == '__main__':
    os.makedirs('.', exist_ok=True)
    gaps = [0.10, 0.20, 0.30]
    for gap in gaps:
        mesh = make_clip(gap)
        filename = f'ps4_cover_clip_direct_gap{int(gap*100):02d}.stl'
        mesh.export(filename)
        print('Exported', filename, 'faces', len(mesh.faces), 'watertight', mesh.is_watertight)
