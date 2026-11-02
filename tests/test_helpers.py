"""Observable helper behavior, without operating hardware or using the network."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/hmi-design-full/scripts'


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def run(name, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / f'{name}.py'), *args], capture_output=True, text=True)


class ContrastTests(unittest.TestCase):
    def test_known_ratios_and_symmetry(self):
        contrast = module('contrast')
        self.assertAlmostEqual(contrast.ratio('#000', '#fff'), 21)
        self.assertAlmostEqual(contrast.ratio('#abc', '#abc'), 1)
        self.assertAlmostEqual(contrast.ratio('#123456', '#abcdef'), contrast.ratio('#abcdef', '#123456'))

    def test_cli_reports_ratio(self):
        result = run('contrast', '#000', '#fff')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('21.00:1', result.stdout)

    def test_invalid_input_is_actionable(self):
        for args in [(), ('#fff',), ('not-a-color', '#fff')]:
            with self.subTest(args=args):
                result = run('contrast', *args)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('Traceback', result.stderr)


class SizingTests(unittest.TestCase):
    def test_physical_conversions(self):
        sizing = module('sizing')
        self.assertAlmostEqual(sizing.mm_to_px(25.4, 150), 150)
        self.assertAlmostEqual(sizing.ppi_from_panel(5, '300x400'), 100)
        for distance in [500, 1000, 2000]:
            mm = sizing.arcmin_to_mm(21, distance)
            self.assertAlmostEqual(sizing.mm_to_arcmin(mm, distance), 21)

    def test_css_pixels_respect_device_pixel_ratio(self):
        result = run('sizing', '--ppi', '200', '--mm', '25.4', '--device-pixel-ratio', '2')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('200 device px = 100 CSS px', result.stdout)

    def test_defaults_and_panel_resolution(self):
        result = run('sizing', '--diag-in', '15.6', '--res', '1920x1080')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('gloved', result.stdout)

    def test_invalid_dimensions_are_rejected(self):
        for args in [('--ppi', '0'), ('--ppi', '-1'), ('--ppi', 'nan'),
                     ('--ppi', '150', '--distance-mm', '0'),
                     ('--ppi', '150', '--device-pixel-ratio', '0'),
                     ('--diag-in', '15', '--res', 'bad'),
                     ('--diag-in', '15', '--res', '0x100'),
                     ('--ppi', '150', '--mm', '20', '--px', '100')]:
            with self.subTest(args=args):
                result = run('sizing', *args)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('Traceback', result.stderr)


class TokenTests(unittest.TestCase):
    def test_scan_skips_tokens_and_build_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'ui.css').write_text('--ink: #ffffff;\nbutton { color: #fff; width: 56px; }\n')
            (root / 'target').mkdir()
            (root / 'target/generated.css').write_text('color: #ff0000;')
            result = run('lint_tokens', tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('ui.css:2:', result.stdout)
            self.assertNotIn('ui.css:1:', result.stdout)
            self.assertNotIn('generated.css', result.stdout)

    def test_file_input_and_invalid_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'view.rs'
            path.write_text('let style = "width: 56px";')
            self.assertIn('56px', run('lint_tokens', str(path)).stdout)
            result = run('lint_tokens', str(path / 'missing'))
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
