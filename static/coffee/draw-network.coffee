$ = jQuery
$(document).ready( ->
  output = Viz($("#network").html(), "svg")
  $("#rendered-graph").html(output)
  w = $("#rendered-graph svg").attr("width")
  val_w = parseInt(w.replace("pt", ""), 10)
  if (val_w > 450)
    $("#main-pane").attr("class", "span12")
)
