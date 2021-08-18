google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Element", "Количество", { role: "style" } ],
    ["4", 100, "#00D575"],
    ["3", 50, "#FE9C4A"],
    ["2", 30, "#FFCB3A"],
    ["1", 60, "#FF3A3A"],
    ["ОТ", 40, "#4C50B8"],
    ["УП", 20, "#9C48C4"],
  ]);

  var view = new google.visualization.DataView(data);
  view.setColumns([0, 1, { calc: "stringify", sourceColumn: 1, type: "string", role: "annotation" }, 2]);

  var options = { width: 630, height: 200, bar: {groupWidth: "100%"}, legend: { position: "none" }, fontSize: 16 };

  // Graph1
  var chart = new google.visualization.ColumnChart(document.getElementById("graph1"));
  chart.draw(view, options);

  // Graph2
  var chart = new google.visualization.ColumnChart(document.getElementById("graph2"));
  chart.draw(view, options);

  // Graph3
  var chart = new google.visualization.ColumnChart(document.getElementById("graph3"));
  chart.draw(view, options);
}