import vl_convert as vlc
from json import JSONDecoder

tasks = {
    "flatten altair images" : render_altair
}

def render_altair(filepath, html, soup, root_element):
    # find all divs with id="altair-viz-####"
    # find all subsequent script elements with type = text/javascript
    # in the content, look for {"$schema" : "...", ...} and parse until closing brace


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


Exampl

<figure class="align-default" id="barplot-mother-tongue" style="width: 700px">
<div class="output text_html">
<style>
  #altair-viz-d2ca5254c4734d559a89086b483dc88f.vega-embed {
    width: 100%;
    display: flex;
  }

  #altair-viz-d2ca5254c4734d559a89086b483dc88f.vega-embed details,
  #altair-viz-d2ca5254c4734d559a89086b483dc88f.vega-embed details summary {
    position: relative;
  }
</style>
<div id="altair-viz-d2ca5254c4734d559a89086b483dc88f"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-d2ca5254c4734d559a89086b483dc88f") {
      outputDiv = document.getElementById("altair-viz-d2ca5254c4734d559a89086b483dc88f");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm/vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm/vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm/vega-lite@5.14.1?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm/vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "5.14.1"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"$schema": "https://vega.github.io/schema/vega/v5.json", "data": [{"name": "source_0", "values": [{"language": "Cree, n.o.s.", "mother_tongue": 64050, "mother_tongue_end": 64050.0, "mother_tongue_start": 0.0}, {"language": "Inuktitut", "mother_tongue": 35210, "mother_tongue_end": 35210.0, "mother_tongue_start": 0.0}, {"language": "Ojibway", "mother_tongue": 17885, "mother_tongue_end": 17885.0, "mother_tongue_start": 0.0}, {"language": "Oji-Cree", "mother_tongue": 12855, "mother_tongue_end": 12855.0, "mother_tongue_start": 0.0}, {"language": "Dene", "mother_tongue": 10700, "mother_tongue_end": 10700.0, "mother_tongue_start": 0.0}, {"language": "Montagnais (Innu)", "mother_tongue": 10235, "mother_tongue_end": 10235.0, "mother_tongue_start": 0.0}, {"language": "Mi'kmaq", "mother_tongue": 6690, "mother_tongue_end": 6690.0, "mother_tongue_start": 0.0}, {"language": "Atikamekw", "mother_tongue": 6150, "mother_tongue_end": 6150.0, "mother_tongue_start": 0.0}, {"language": "Plains Cree", "mother_tongue": 3065, "mother_tongue_end": 3065.0, "mother_tongue_start": 0.0}, {"language": "Stoney", "mother_tongue": 3025, "mother_tongue_end": 3025.0, "mother_tongue_start": 0.0}]}, {"name": "source_0_x_domain_language", "values": [{"language": "Cree, n.o.s."}, {"language": "Inuktitut"}, {"language": "Ojibway"}, {"language": "Oji-Cree"}, {"language": "Dene"}, {"language": "Montagnais (Innu)"}, {"language": "Mi'kmaq"}, {"language": "Atikamekw"}, {"language": "Plains Cree"}, {"language": "Stoney"}]}], "signals": [{"name": "x_step", "value": 20}, {"name": "width", "update": "bandspace(domain('x').length, 0.1, 0.05) * x_step"}], "marks": [{"type": "rect", "name": "marks", "from": {"data": "source_0"}, "encode": {"update": {"ariaRoleDescription": {"value": "bar"}, "y": {"field": "mother_tongue_end", "scale": "y"}, "fill": {"value": "#4c78a8"}, "description": {"signal": "\"language: \" + (isValid(datum[\"language\"]) ? datum[\"language\"] : \"\"+datum[\"language\"]) + \"; mother_tongue: \" + (format(datum[\"mother_tongue\"], \"\"))"}, "x": {"field": "language", "scale": "x"}, "width": {"signal": "max(0.25, bandwidth('x'))"}, "y2": {"field": "mother_tongue_start", "scale": "y"}}}, "style": ["bar"]}], "scales": [{"name": "x", "type": "band", "domain": {"data": "source_0_x_domain_language", "field": "language", "sort": true}, "range": {"step": {"signal": "x_step"}}, "paddingOuter": 0.05, "paddingInner": 0.1}, {"name": "y", "type": "linear", "domain": {"fields": ["mother_tongue_start", "mother_tongue_end"], "data": "source_0"}, "range": [{"signal": "height"}, 0], "zero": true, "nice": true}], "axes": [{"scale": "y", "orient": "left", "gridScale": "x", "domain": false, "labels": false, "tickCount": {"signal": "ceil(height/40)"}, "maxExtent": 0, "ticks": false, "grid": true, "zindex": 0, "minExtent": 0, "aria": false}, {"scale": "x", "labelAlign": "right", "title": "language", "orient": "bottom", "labelAngle": 270, "labelBaseline": "middle", "zindex": 0, "grid": false}, {"scale": "y", "zindex": 0, "grid": false, "title": "mother_tongue", "orient": "left", "labelOverlap": true, "tickCount": {"signal": "ceil(height/40)"}}], "padding": 5, "style": "cell", "height": 300, "background": "white"}, {"mode": "vega"});
</script></div><figcaption>
<p><span class="caption-number">Fig. 1.8 </span><span class="caption-text">Bar plot of the ten Aboriginal languages most often reported by Canadian residents as their mother tongue</span><a class="headerlink" href="#barplot-mother-tongue" title="Permalink to this image">#</a></p>
</figcaption>
</figure>

