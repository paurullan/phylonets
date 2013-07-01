###
For the remote soft calculation procedure
variables:
1. INTERVAL_TIME = ms for the next call
2. MAX_CALLS
3. '#calc_spinner' for the div animation
4. '#calc_result' for where to place the calculation
5. call_url
###
$ = jQuery

result_families_func = (val) ->

  $("#calc_families_spinner").hide()
  if (!val)
    val = "Cannot generate tree-child family"
    $("#families_field").show()
    $("#families_field").html(val)
    $("#tree-child-message-no").show()
  else
    how_many = val.length
    $("#tree-child-number").html(how_many)
    $("#tree-child-message-yes").show()
    for family, i in val
       s = "#family-#{ i }"
       output = Viz(family, "svg")
       div = """<div class="tree-child-graph" id="#{ s }">#{ output }</div>"""
       $("#rendered-families").append(div)

$(document).ready( ->
  MAX_CALLS = 12 * 15  # 15min
  INTERVAL_TIME = 5000
  job_families_url = "/job/families/"
  network_url = "#{job_families_url}#{queue_id}/#{families_job_id}"
  call_counter = 0

  $.getJSON(network_url, (result) ->
    if (result['status'] == 'done')
      result_families_func(result['value'])
    else
      interval = setInterval( ->
        $.getJSON(network_url, (result) ->
          if (result['status'] == 'done')
            result_families_func(result['value'])
            clearInterval(interval)
          else
            call_counter += 1
            if (call_counter > MAX_CALLS)
              clearInterval(interval)
              $("#calc_families_spinner").hide()
              $("#families_field").html("Something went wrong")
        )
      , INTERVAL_TIME)
  )
)
