//////////////////////////////////////////////////////////////////
/////   D3 長條圖
//////////////////////////////////////////////////////////////////

nv.addGraph(function () {
    var chart = nv.models.discreteBarChart();
    chart.color(d3.scale.category10().range())  // 圖表色彩主題
        .staggerLabels(true)    // 避免Y軸文字於窄畫面打架
        .showValues(true);      // 於每個長條上顯示數值
    // X, Y軸座標軸設定
    chart.xAxis;
    chart.yAxis.tickFormat(d3.format("d"));
    // 滑鼠指過去顯示資料
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
    // Html DOM 繪圖
    d3.select('#discreteBarChart svg')
        .datum(data_discreteBarChart)
        .transition().duration(500)
        .attr('height', 400)
        .style("font-size", "20px")
        .call(chart);
    // X 軸字體樣式
    d3.select('.nv-x.nv-axis > g').selectAll('g')
        .selectAll('text')
        .style('text-align', "right")
        .attr('transform', function(d,i,j) { return 'translate (0, 10)' });

    // 這邊開始為點選長條後的發光效果
    // 在Html中插入<defs></defs>
    // 是SVG filter 的特殊處理方式，在欲使用之SVG元素加入style="filter:url(#white-glow);"即可
    filter = d3.select('defs')
        .append("filter")
        .attr("id", "white-glow")
        .attr("x", "-5000%")
        .attr("y", "-5000%")
        .attr("width", "10000%")
        .attr("height", "10000%");
        
    filter.append('feFlood')
        .attr('result', 'flood')
        .attr('flood-color', '#ffffff') // 發光的顏色
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

    nv.utils.windowResize(chart.update); // 響應式圖表

    return chart;
});

// Event Listener為非同步，等待圖表繪製完成後再存取DOM
document.addEventListener("DOMContentLoaded", function(e){
    var bars = document.getElementsByClassName("discreteBar");
    bars[0].style.filter = "url(#white-glow)";
    var i;
    for(i = 0; i < bars.length; i++){
        bars[i].setAttribute("onclick", "clickBar(" + i + ","+ bars.length + ")" );
    }
})
// 點擊後處發函式: i: 第i個主題, length: 主題總數 即長條總數
function clickBar(i, length){
    var id = "topic-" + i.toString();
    document.getElementById(id).classList.remove("uk-hidden"); // 顯示該主題頁面
    var clickedElement = document.getElementsByClassName("discreteBar");   
    try{glow(clickedElement[i]);} // 使其發光
    catch(e){console.log(e);}
    var j;
    for(j = 0; j < length; j++){
        if(j != i){
            unglow(clickedElement[j]);  // 使其他長條不發光
            document.getElementById("topic-" + j.toString()).classList.add("uk-hidden"); // 隱藏其他主題頁面
        }
    }
}
// 發光
function glow(clickedElement){
    var style = clickedElement.style;
    style.filter = "url(#white-glow)";
}
// 不發光
function unglow(clickedElement){
    var style = clickedElement.style;
    style.filter = "none";
}

