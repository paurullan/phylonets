$ = jQuery
$(document).ready( ->
  $(":file").filestyle()

  $("#hide-graph-names").click( -> $("#rendered-graph text").toggle() )

)
