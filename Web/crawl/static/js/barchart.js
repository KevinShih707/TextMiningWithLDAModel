//////////////////////////////////////////////////////////////////
/////   D3 長條圖
//////////////////////////////////////////////////////////////////

nv.addGraph(function () {
    var chart = nv.models.discreteBarChart();
    chart.color(d3.scale.category10().range())
        .staggerLabels(true);
    chart.xAxis;
    chart.yAxis.tickFormat(d3.format("d"));
    chart.tooltipContent(function (key, y, e, graph) {
        var x = String(graph.point.x);
        var y = String(graph.point.y);
        if (key == 'Serie 1') {
            var y = graph.point.y;
        }
        tooltip_str = '<center><b>' + x + '</b></center>' + '篇數:' + y;
        return tooltip_str;
    });
    chart.margin({"left":30,"right":0,"top":30,"bottom":70});
    d3.select('#discreteBarChart svg')
        .datum(data_discreteBarChart)
        .transition().duration(500)
        .attr('height', 400)
        .style("font-size", "20px")
        .call(chart);

    d3.select('.nv-x.nv-axis > g').selectAll('g')
        .selectAll('text')
        .style('text-align', "right")
        .attr('transform', function(d,i,j) { return 'translate (0, 10)' });

    filter = d3.select('defs')
        .append("filter")
        .attr("id", "white-glow")
        .attr("x", "-5000%")
        .attr("y", "-5000%")
        .attr("width", "10000%")
        .attr("height", "10000%");
        
    filter.append('feFlood')
        .attr('result', 'flood')
        .attr('flood-color', '#ffffff')
        .attr('flood-opacity', '1');

    filter.append('feComposite')
        .attr('in', 'flood')
        .attr('result', 'mask')
        .attr('in2', 'SourceGraphic')
        .attr('operator', 'in');

    filter.append('feMorphology')
        .attr('in', 'mask')
        .attr('result', 'dilated')
        .attr('operator', 'dilate')
        .attr('radius', '2');

    filter.append('feGaussianBlur')
        .attr('in', 'dilated')
        .attr('result', 'blurred')
        .attr('stdDeviation', '5');

    feMerge = filter.append('feMerge')
        .append('feMergeNode')
        .attr('in', 'blurred');

    feMerge.append('feMergeNode')
        .attr('in', 'SourceGraphic');

    nv.utils.windowResize(chart.update);

    return chart;
});

document.addEventListener("DOMContentLoaded", function(e){
    var bars = document.getElementsByClassName("discreteBar");
    bars[0].style.filter = "url(#white-glow)";
    var i;
    for(i = 0; i < bars.length; i++){
        bars[i].setAttribute("onclick", "clickBar(" + i + ","+ bars.length + ")" );
    }
})

function clickBar(i, length){
    var id = "topic-" + i.toString();
    document.getElementById(id).classList.remove("uk-hidden");
    var clickedElement = document.getElementsByClassName("discreteBar");    
    try{glow(clickedElement[i]);}
    catch(e){console.log(e);}
    var j;
    for(j = 0; j < length; j++){
        if(j != i){
            unglow(clickedElement[j]);
            document.getElementById("topic-" + j.toString()).classList.add("uk-hidden");
        }
    }
}

function glow(clickedElement){
    var style = clickedElement.style;
    style.filter = "url(#white-glow)";
}

function unglow(clickedElement){
    var style = clickedElement.style;
    style.filter = "none";
}

