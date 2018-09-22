////////////////////////////////////
//Responsive D3 Charts
////////////////////////////////////
var allD3 = d3.select(".d3-RWD");

var container = d3.select(allD3.node().parentNode),
    width = parseInt(allD3.style("width")),
    height = parseInt(allD3.style("height")),
    aspect = width / height;

// add viewBox and preserveAspectRatio properties,
// and call resize so that svg resizes on inital page load
allD3.attr("viewBox", "0 0 " + width + " " + height)
    .attr("perserveAspectRatio", "xMinYMid")
    .call(resize);

// to register multiple listeners for same event type,
// you need to add namespace, i.e., 'click.foo'
// necessary if you call invoke this function for multiple svgs
// api docs: https://github.com/mbostock/d3/wiki/Selections#on
d3.select(window).on("resize." + container.attr("id"), resize);

// get width of container and resize svg to fit it
function resize() {
    var targetWidth = parseInt(container.style("width"));
    allD3.attr("width", targetWidth);
    allD3.attr("height", Math.round(targetWidth / aspect));
}