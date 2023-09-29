import vl_convert as vlc


def render_altair_images():
    # find all divs with id="altair-viz-####"
    # find all subsequent script elements with type = text/javascript
    # in the content, look for {"$schema" : "...", ...} and parse until closing brace

from json import JSONDecoder

def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

vl_spec = r"""
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"url": "data/movies.json"},
  "mark": "circle",
  "encoding": {
    "x": {
      "bin": {"maxbins": 10},
      "field": "IMDB Rating"
    },
    "y": {
      "bin": {"maxbins": 10},
      "field": "Rotten Tomatoes Rating"
    },
    "size": {"aggregate": "count"}
  }
}
"""

png_data = vlc.vegalite_to_png(vl_spec=vl_spec, scale=2)

fn vegalite_to_png(
    vl_spec: PyObject,
    vl_version: Option<&str>,
    scale: Option<f32>,
    ppi: Option<f32>,
    config: Option<PyObject>,
    theme: Option<String>,
    show_warnings: Option<bool>,
) -> PyResult<PyObject> 

/// Convert a Vega-Lite spec to PNG image data using a particular
/// version of the Vega-Lite JavaScript library.
///
/// Args:
///     vl_spec (str | dict): Vega-Lite JSON specification string or dict
///     vl_version (str): Vega-Lite library version string (e.g. 'v5.5')
///         (default to latest)
///     scale (float): Image scale factor (default 1.0)
///     ppi (float): Pixels per inch (default 72)
///     config (dict | None): Chart configuration object to apply during conversion
///     theme (str | None): Named theme (e.g. "dark") to apply during conversion
///     show_warnings (bool | None): Whether to print Vega-Lite compilation warnings (default false)
/// Returns:
///     bytes: PNG image data

////////////////////////////

/// Convert a Vega spec to PNG image data.
///
/// Args:
///     vg_spec (str | dict): Vega JSON specification string or dict
///     scale (float): Image scale factor (default 1.0)
///     ppi (float): Pixels per inch (default 72)
///
/// Returns:
///     bytes: PNG image data
#[pyfunction]
#[pyo3(text_signature = "(vg_spec, scale, ppi)")]
fn vega_to_png(vg_spec: PyObject, scale: Option<f32>, ppi: Option<f32>) -> PyResult<PyObject>
