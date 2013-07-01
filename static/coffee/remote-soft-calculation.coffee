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

$(document).ready( ->
  job_soft_url = "/job/soft/"

  if soft_too_expensive
    $("#calc_soft_spinner").hide()
    $("#cluster_soft_too_expensive").show()
    return

  result_func = (val) ->
    $("#calc_soft_spinner").hide()
    $("#cluster_softwired_field").show()
    $("#cluster_softwired_field_pre").html(val)

  MAX_CALLS = 12 * 15  # 15min
  INTERVAL_TIME = 5000
  #  job_url = "http://localhost:8080/job/soft/"
  network_url = "#{job_soft_url}#{queue_id}/#{soft_job_id}"
  call_counter = 0

  $.getJSON(network_url, (result) ->
    if (result['status'] == 'done')
      result_func(result['value'])
    else
      interval = setInterval( ->
        $.getJSON(network_url, (result) ->
          if (result['status'] == 'done')
            result_func(result['value'])
            clearInterval(interval)
          else
            call_counter += 1
            if (call_counter > MAX_CALLS)
              clearInterval(interval)
              $("#calc_soft_spinner").hide()
              $("#cluster_softwired_field").html("Something went wrong")
        )
      , INTERVAL_TIME)
  )
)
