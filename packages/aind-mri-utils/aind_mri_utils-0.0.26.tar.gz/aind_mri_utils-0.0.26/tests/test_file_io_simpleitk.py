import os
import unittest
from pathlib import Path

import numpy as np

from aind_mri_utils.file_io import simpleitk as si
from aind_mri_utils.optimization import create_rigid_transform


class SITKTest(unittest.TestCase):
    """Tests functions in `file_io.simpleitk`."""

    def test_save_sitk_transform(self) -> None:
        """
        Tests that the `save_sitk_transform` function works as intended.
        """
        # Test that a 4x3 transform is created correctly
        trans = create_rigid_transform(0, 0, 0, 0, 0, 0)
        self.assertTrue(np.array_equal(trans[:3, :3], np.eye(3)))
        si.save_sitk_transform(str(Path("testsave.h5")), trans)
        load_trans = si.load_sitk_transform(str(Path("testsave.h5")))
        self.assertTrue(self.close_enough(trans, load_trans))

        # Test that the above can work from 6x1
        si.save_sitk_transform(str(Path("testsave.h5")), [0, 0, 0, 0, 0, 0])
        load_trans = si.load_sitk_transform(str(Path("testsave.h5")))
        self.assertTrue(self.close_enough(trans, load_trans))

        # Test more complicated transform
        trans[0, -1] = 1
        si.save_sitk_transform(str(Path("testsave.h5")), trans)
        load_trans = si.load_sitk_transform(str(Path("testsave.h5")))
        self.assertTrue(self.close_enough(trans, load_trans))

        # Test inversion functionality when saving
        si.save_sitk_transform(
            str(Path("testsave.h5")), trans, transpose_matrix=True
        )
        load_trans = si.load_sitk_transform(str(Path("testsave.h5")))
        load_trans[:3, :3] = load_trans[:3, :3].T

        self.assertTrue(np.array_equal(trans, load_trans))

        # Test inversion functionality when loading
        si.save_sitk_transform(
            str(Path("testsave.h5")), trans, transpose_matrix=True
        )
        load_trans = si.load_sitk_transform(
            str(Path("testsave.h5")), transpose_matrix=True
        )

        self.assertTrue(self.close_enough(trans, load_trans))

        # Test failure modes
        trans = np.eye(4)
        try:
            si.save_sitk_transform(str(Path("testsave.h5")), trans)
        except NotImplementedError:
            self.assertTrue(True)

        try:
            load_trans = si.load_sitk_transform(
                str(Path("testsave.h5")), outshape=(4, 4)
            )
        except NotImplementedError:
            self.assertTrue(True)

        # Kill the file we created- it was just a test
        os.remove("testsave.h5")

    def close_enough(self, a, b):
        """Helper function to check if two arrays are close enough."""
        return np.all(np.abs(a - b) < 0.0001)


if __name__ == "__main__":
    unittest.main()
