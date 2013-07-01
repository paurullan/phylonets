// Generated by CoffeeScript 1.4.0

/*
For the remote soft calculation procedure
variables:
1. INTERVAL_TIME = ms for the next call
2. MAX_CALLS
3. '#calc_spinner' for the div animation
4. '#calc_result' for where to place the calculation
5. call_url
*/


(function() {
  var $;

  $ = jQuery;

  $(document).ready(function() {
    var INTERVAL_TIME, MAX_CALLS, call_counter, job_soft_url, network_url, result_func;
    job_soft_url = "/job/soft/";
    if (soft_too_expensive) {
      $("#calc_soft_spinner").hide();
      $("#cluster_soft_too_expensive").show();
      return;
    }
    result_func = function(val) {
      $("#calc_soft_spinner").hide();
      $("#cluster_softwired_field").show();
      return $("#cluster_softwired_field_pre").html(val);
    };
    MAX_CALLS = 12 * 15;
    INTERVAL_TIME = 5000;
    network_url = "" + job_soft_url + queue_id + "/" + soft_job_id;
    call_counter = 0;
    return $.getJSON(network_url, function(result) {
      var interval;
      if (result['status'] === 'done') {
        return result_func(result['value']);
      } else {
        return interval = setInterval(function() {
          return $.getJSON(network_url, function(result) {
            if (result['status'] === 'done') {
              result_func(result['value']);
              return clearInterval(interval);
            } else {
              call_counter += 1;
              if (call_counter > MAX_CALLS) {
                clearInterval(interval);
                $("#calc_soft_spinner").hide();
                return $("#cluster_softwired_field").html("Something went wrong");
              }
            }
          });
        }, INTERVAL_TIME);
      }
    });
  });

}).call(this);