import script
import pytest
from gi.repository import GLib  # noqa: E402


def test_run_command():
    assert script.run("echo testest") == "testest"


expected_css = """label {
  color: rgb(255,0,0);
  padding-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
  padding-top: 10px;
}
"""


def test_parse_output():
    output = "label\ncolor:red;\npadding:10px;"
    (label, css) = script.parse_output(output)
    assert label == "label"
    assert css.to_string() == expected_css


def test_parse_output_no_label():
    output = "\ncolor:red;\npadding:10px;"
    (label, css) = script.parse_output(output)
    assert label == ""
    assert css.to_string() == expected_css


def test_parse_output_no_css():
    output = "label"
    (label, css) = script.parse_output(output)
    assert label == "label"
    assert css is None


def test_parse_output_invalid_css():
    output = "label\ncolor:red;\npadding:10xd"  # no semicolon
    with pytest.raises(GLib.Error):
        script.parse_output(output)
