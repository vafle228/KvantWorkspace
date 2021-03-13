google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Element", "Оценка", { role: "style" } ],
    ["01", 4, "#00D575"],
    ["02", 3, "#FE9C4A"],
    ["03", 2, "#FFCB3A"],
    ["04", 0, "#FF3A3A"],
    ["05", 4, "#00D575"],
    ["06", 3, "#FE9C4A"],
    ["07", 2, "#FFCB3A"],
    ["08", 1, "#FF3A3A"],
    ["07", 2, "#FFCB3A"],
    ["08", 1, "#FF3A3A"],
    ["09", 0, "#00D575"],
    ["10", 3, "#FE9C4A"],
    ["11", 2, "#FFCB3A"],
    ["12", 1, "#FF3A3A"],
    ["13", 2, "#FFCB3A"],
    ["14", 2, "#FE9C4A"],
    ["15", 2, "#FFCB3A"],
    ["16", 1, "#FF3A3A"],
    ["17", 2, "#FFCB3A"],
    ["18", 1, "#FF3A3A"],
    ["19", 4, "#00D575"],
    ["20", 0, "#FE9C4A"],
    ["21", 0, "#FFCB3A"],
    ["22", 1, "#FF3A3A"],
    ["23", 1, "#FF3A3A"],
    ["24", 2, "#FFCB3A"],
    ["25", 3, "#FE9C4A"],
    ["26", 2, "#FFCB3A"],
    ["27", 1, "#FF3A3A"],
    ["28", 2, "#FFCB3A"],
    ["01", 1, "#FF3A3A"],
    ["02", 4, "#00D575"],
    ["03", 3, "#FE9C4A"],
    ["04", 2, "#FFCB3A"],
    ["05", 1, "#FF3A3A"],
  ]);

  var view = new google.visualization.DataView(data);
  view.setColumns([0, 1, { calc: "stringify", sourceColumn: 1, type: "string", role: "annotation" }, 2]);

  var options = { width: 730, height: 200, bar: {groupWidth: "100%"}, legend: { position: "none" }, };

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