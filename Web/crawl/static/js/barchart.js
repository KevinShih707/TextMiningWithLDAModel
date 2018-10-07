//////////////////////////////////////////////////////////////////
/////   D3 長條圖
//////////////////////////////////////////////////////////////////

nv.addGraph(function () {
    var chart = nv.models.discreteBarChart();
    chart.color(d3.scale.category10().range())
        .staggerLabels(true);
    chart.xAxis;
    chart.yAxis.tickFormat(d3.format('.5f'));
    chart.tooltipContent(function (key, y, e, graph) {
        var x = String(graph.point.x);
        var y = String(graph.point.y);
        if (key == 'Serie 1') {
            var y = String( Math.round(graph.point.y * 1000000) / 1000000);
        }
        tooltip_str = '<center><b>' + x + '</b></center>' + '概率:' + y;
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
