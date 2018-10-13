//////////////////////////////////////////////////////////////////
/////   D3 泡泡圖
//////////////////////////////////////////////////////////////////

var svg = d3.select("#chart");
var diameter = +svg.attr("width");
var margin = 100;
var g = svg.append("g").attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")")
    .style("transform", "translate(50%, 50%)");
document.getElementById("chart").style.opacity = 0; // 透明度先設成0

/* 色彩Iterator */
var color = d3.scaleOrdinal().domain([0, 1]).range(['#b3b3b3', '#e6e6e6']);
var small_color = d3.scaleOrdinal(d3.schemeCategory10);

var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(2);

var jsonPath = "/bubble_json/site=" + office + "&theme=" + classification + "/";
console.log(jsonPath);

/* 讀JSON畫圖 */
d3.json(jsonPath, function(error, root) {
    if (error) throw error;

    root = d3.hierarchy(root)
        .sum(function(d) { return d.size; })
        .sort(function(a, b) { return b.value - a.value; });

    var focus = root;
    var nodes = pack(root).descendants();
    var view;

    /* 非同步畫圓，頁面其餘元素先行載入 */
    var circle = g.selectAll("circle")
    .data(nodes)
    .enter().append("circle")
        .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
        .style("fill", function(d, i) { 
            // console.log(d.children);
            document.getElementById("bubble-loader-wrapper").hidden = true;   // 載入完畢，隱藏Spinner
            chart = document.getElementById("chart");           // 載入後淡入效果, 滑~~順~~
            fadein(chart);  // 淡入圖表
            return d.children ? color(d.depth) : small_color(i); })
        .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); });

    // var circle = g.selectAll(".node--leaf")
    // .style("fill", small_color);

    /* 放上文字 */
    var text = g.selectAll("text")
    .data(nodes)
    .enter().append("text")
        .attr("class", "label")
        .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
        .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
        .text(function(d) { return d.data.name; });

    var node = g.selectAll("circle,text");

    /* 背景顏色與網頁背景一樣 */
    svg
        .style("background", "#222222")
        .on("click", function() { zoom(root); });

    zoomTo([root.x, root.y, root.r * 2 + margin]);

    /* 控制縮放 */
    function zoom(d) {
        var focus0 = focus; focus = d;

        var transition = d3.transition()
            .duration(d3.event.altKey ? 7500 : 750)
            .tween("zoom", function(d) {
                var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
                return function(t) { zoomTo(i(t)); };
            });

        transition.selectAll("text")
            .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
            .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
            .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
            .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
    }

    function zoomTo(v) {
        var k = diameter / v[2]; view = v;
        node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
        circle.attr("r", function(d) { return d.r * k; });
    }
});

/* 淡入效果 */
function fadein(element) {
    var op = 0.1;  // initial opacity
    element.style.display = 'block';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 10);
}
