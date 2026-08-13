import os
import trimesh

BASE = '/workspaces/-'

cover_path = os.path.join(BASE, 'ps4_cover_with_latch_slots.stl')

# Press-fit target: 0.1-0.2 mm radial clearance overall.
# For a ~3.2 mm shaft, we use 3.4 mm hole and 3.2 mm shaft.
# This corresponds to 0.1 mm radial gap (0.2 mm on diameter).
HOLE_RADIUS = 1.70
SHAFT_RADIUS = 1.60
SHAFT_HEIGHT = 4.5
BASE_THICKNESS = 2.2
COVER_HOLE_DEPTH = 12.0

cover = trimesh.load(cover_path, force='mesh')
cover = cover.copy()
min_xyz = cover.bounds[0]
max_xyz = cover.bounds[1]

# Use the same 4 corner positions as the existing latch system.
positions = [
    [min_xyz[0] + 18.0, min_xyz[1] + 22.0, 0.0],
    [max_xyz[0] - 18.0, min_xyz[1] + 22.0, 0.0],
    [min_xyz[0] + 18.0, max_xyz[1] - 22.0, 0.0],
    [max_xyz[0] - 18.0, max_xyz[1] - 22.0, 0.0],
]

# Create the 4 holes in the cover body without affecting ventilation apertures.
hole_meshes = []
for px, py, pz in positions:
    cyl = trimesh.creation.cylinder(radius=HOLE_RADIUS, height=COVER_HOLE_DEPTH, sections=64)
    cyl.apply_translation([px, py, pz])
    hole_meshes.append(cyl)

for cyl in hole_meshes:
    cover = cover.difference(cyl, engine='manifold')

cover.export(os.path.join(BASE, 'Cover_without_texture_final.stl'))
print('Saved cover:', os.path.join(BASE, 'Cover_without_texture_final.stl'))

# Build a hidden press-fit clip set: small shaft sits inside shell and is not visible from the outside.
clip_part = []
for px, py, pz in positions:
    base_plate = trimesh.creation.box(extents=(10.0, 10.0, BASE_THICKNESS))
    base_plate.apply_translation([px, py, 1.1])

    shaft = trimesh.creation.cylinder(radius=SHAFT_RADIUS, height=SHAFT_HEIGHT, sections=64)
    shaft.apply_translation([px, py, -2.0])

    # add a slight retention lip to hold the clip firmly without visible parts
    lip = trimesh.creation.cylinder(radius=SHAFT_RADIUS + 0.25, height=1.0, sections=64)
    lip.apply_translation([px, py, -0.2])

    clip_part.append(trimesh.util.concatenate([base_plate, shaft, lip]))

clip_set = trimesh.util.concatenate(clip_part)
clip_set.export(os.path.join(BASE, 'ps4_test_detal_final_hidden_clips.stl'))
print('Saved clips:', os.path.join(BASE, 'ps4_test_detal_final_hidden_clips.stl'))

# preview assembly
assembly = trimesh.util.concatenate([cover, clip_set])
assembly.export(os.path.join(BASE, 'assembly_hidden_clips_preview.stl'))
print('Saved preview:', os.path.join(BASE, 'assembly_hidden_clips_preview.stl'))
print('Cover watertight:', cover.is_watertight)
print('Clip set watertight:', clip_set.is_watertight)
print('Press-fit target: hole radius %.2f, shaft radius %.2f, radial gap %.2f mm' % (HOLE_RADIUS, SHAFT_RADIUS, HOLE_RADIUS-SHAFT_RADIUS))
