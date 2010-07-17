
function showTooltip(x, y, contents) {
    $('<div id="tooltip">' + contents + '</div>').css( {
        position: 'absolute',
        display: 'none',
        top: y + 5,
        left: x + 5,
        border: '1px solid #fdd',
        padding: '2px',
        'background-color': '#fee',
        opacity: 0.80
    }).appendTo("body").fadeIn(200);
}

function bindTooltip(chart, info) {
    var previousPoint = null;
    chart.bind("plothover", function (event, pos, item) {
        if (item) {
            if (previousPoint != item.datapoint) {
                curInfo = info[item.seriesIndex][item.dataIndex];

                previousPoint = item.datapoint;
                
                $("#tooltip").remove();
                
                showTooltip(item.pageX, item.pageY,
                            curInfo[1]);
            }
        }
        else {
            $("#tooltip").remove();
            previousPoint = null;            
        }
    });
}
