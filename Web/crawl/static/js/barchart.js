//////////////////////////////////////////////////////////////////
/////   D3 長條圖
//////////////////////////////////////////////////////////////////

nv.addGraph(function () {
    var chart = nv.models.discreteBarChart();
    chart.color(d3.scale.category10().range());
    chart.xAxis
    chart.yAxis
    chart.tooltipContent(function (key, y, e, graph) {
        var x = String(graph.point.x);
        var y = String(graph.point.y);
        if (key == 'Serie 1') {
            var y = String( Math.round(graph.point.y * 1000000) / 1000000);
        }
        tooltip_str = '<center><b>' + x + '</b></center>' + '概率:' + y;
        console.log(Math.round(y * 10) / 10);
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
    .attr('style', "text-align: right")
    .attr('transform', function(d,i,j) { return 'translate (-10, 10) rotate(30 0,0)' });
  
    
    return chart;
});
