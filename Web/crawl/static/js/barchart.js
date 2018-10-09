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
  
    nv.utils.windowResize(chart.update);

    return chart;
});

document.addEventListener("DOMContentLoaded", function(e){
    var bars = document.getElementsByClassName("nv-bar");
    var i;
    for(i = 0; i < bars.length; i++){
        console.log("var i", i);
        bars[i].setAttribute("onclick", "clickBar(" + i + ","+ bars.length + ")" );
    }
})

function clickBar(i, length){
    var id = "topic-" + i.toString();
    console.log(i, length);
    document.getElementById(id).classList.remove("uk-hidden");
    var j;
    for(j = 0; j < length; j++){
        if(j != i){
            console.log(j)
            document.getElementById("topic-" + j.toString()).classList.add("uk-hidden");
        }
    }
}

