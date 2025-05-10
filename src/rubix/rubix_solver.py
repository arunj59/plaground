from copy import deepcopy

# Corner indices (0-7) mapped as:
#    0: UFR, 1: URB, 2: UBL, 3: ULF
#    4: DFR, 5: DRB, 6: DBL, 7: DLF

class RubiksMini:
    def __init__(self, state=None):
        self.corner_indices = list(range(8))
        self.corner_orientations = [0] * 8  # 0 = correct, 1/2 = twisted
        if state:
            self.corner_indices, self.corner_orientations = state

    def rotate_face(self, face):
        # face: 'R', 'U', 'F', etc.
        # Define face corner mapping and orientation effect
        moves = {
            'R':  ([0, 1, 5, 4], [2, 1, 2, 1]),
            'R\'': ([4, 5, 1, 0], [1, 2, 1, 2]),
            'U':  ([0, 3, 2, 1], [0, 0, 0, 0]),
            'U\'': ([1, 2, 3, 0], [0, 0, 0, 0]),
            'F':  ([0, 4, 7, 3], [1, 2, 1, 2]),
            'F\'': ([3, 7, 4, 0], [2, 1, 2, 1]),
        }

        corners, orientation_shifts = moves[face]
        temp_indices = deepcopy(self.corner_indices)
        temp_orients = deepcopy(self.corner_orientations)

        for i in range(4):
            self.corner_indices[corners[i]] = temp_indices[corners[(i + 3) % 4]]
            shift = orientation_shifts[i]
            self.corner_orientations[corners[i]] = (temp_orients[corners[(i + 3) % 4]] + shift) % 3

    def apply_moves(self, moves):
        for m in moves.split():
            self.rotate_face(m)

    def print_state(self):
        print("Corners:", self.corner_indices)
        print("Orientations:", self.corner_orientations)

    def is_solved(self):
        return self.corner_indices == list(range(8)) and all(o == 0 for o in self.corner_orientations)


def demo_solver():
    print("🔄 Scrambling the cube...")
    cube = RubiksMini()
    scramble = "R U R' U R U2 R' F R' F' U'"
    cube.apply_moves(scramble)
    cube.print_state()

    print("\n🧠 Applying solution steps (layered method)...")

    # From the PDF guide:
    step1 = "R' D' R"       # Place white corners
    step2 = "R U R' U R U2 R'"  # Yellow face
    step3 = "R' F R' B2 R F' R' B2 R2"  # Yellow corners

    cube.apply_moves(step1)
    cube.apply_moves(step2)
    cube.apply_moves(step3)

    print("\n✅ Final Cube State:")
    cube.print_state()
    print("\n🎉 Solved?" , cube.is_solved())


# Run the full solver demo
demo_solver()
