import unittest
from unittest.mock import patch, MagicMock

import dockreap.__main__ as dockreap_main


class TestDockreapMain(unittest.TestCase):
    def test_get_anonymous_volumes_filters_64char_hex(self):
        fake_stdout = "\n".join(
            [
                "short",
                "nothex" * 10,
                "a" * 64,  # valid
                "A" * 64,  # invalid (uppercase not matched)
                "g" * 64,  # invalid (not hex)
                "b" * 63,  # invalid (too short)
                "c" * 65,  # invalid (too long)
                "deadbeef" * 8,  # valid 64-char hex
            ]
        )

        completed = MagicMock()
        completed.stdout = fake_stdout

        with patch.object(dockreap_main.subprocess, "run", return_value=completed) as run_mock:
            vols = dockreap_main.get_anonymous_volumes()

        # Ensure docker command was called correctly
        run_mock.assert_called_with(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            stdout=dockreap_main.subprocess.PIPE,
            text=True,
        )

        self.assertEqual(vols, ["a" * 64, "deadbeef" * 8])

    def test_is_volume_used_true_when_docker_returns_container_ids(self):
        completed = MagicMock()
        completed.stdout = "abc123\n"

        with patch.object(dockreap_main.subprocess, "run", return_value=completed):
            self.assertTrue(dockreap_main.is_volume_used("x" * 64))

    def test_is_volume_used_false_when_no_container_ids(self):
        completed = MagicMock()
        completed.stdout = "\n"

        with patch.object(dockreap_main.subprocess, "run", return_value=completed):
            self.assertFalse(dockreap_main.is_volume_used("x" * 64))

    def test_cleanup_symlink_does_nothing_when_not_symlink(self):
        # We don't want to touch the real filesystem, so we patch the Path object
        fake_data_path = MagicMock()
        fake_data_path.is_symlink.return_value = False

        fake_volume_dir = MagicMock()
        fake_volume_dir.__truediv__.side_effect = lambda x: fake_data_path if x == "_data" else MagicMock()

        with patch.object(dockreap_main, "VOLUME_BASE_PATH") as base_path_mock:
            base_path_mock.__truediv__.return_value = fake_volume_dir

            # Should not raise; should not try to unlink/rmtree
            dockreap_main.cleanup_symlink("a" * 64)

        fake_data_path.unlink.assert_not_called()


if __name__ == "__main__":
    unittest.main()
