// Generated by CoffeeScript 1.4.0
(function() {
  var $;

  $ = jQuery;

  $(document).ready(function() {
    var output, val_w, w;
    output = Viz($("#network").html(), "svg");
    $("#rendered-graph").html(output);
    w = $("#rendered-graph svg").attr("width");
    val_w = parseInt(w.replace("pt", ""), 10);
    if (val_w > 450) {
      return $("#main-pane").attr("class", "span12");
    }
  });

}).call(this);
