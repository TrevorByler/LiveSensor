$(document).ready(function() {
  $.ajax({
    url: "http://localhost/chart_data.php",
    type: "GET",
    dataType: "json",
    success: function(data) {
      chartData = data;
      const chartConfig = {
      type: 'line',
      renderAt: 'chart-container',
      width: '100%',
      height: '400',
      dataFormat: 'json',
      dataSource: {
        // Chart Configuration
        "chart": {
            "caption": "Room Brightness",
            "xAxisName": "Timestamp",
            "yAxisName": "Level of Visible Light",
            "theme": "fusion",
            },
        // Chart Data
        "data": chartData
        }
    };
      var apiChart = new FusionCharts(chartConfig);
      apiChart.render();
    }
  });
});
