<!-- venim d'un row i tenim 12 spans -->

% setdefault('title', "Analyzing phylogenetic network")

% setdefault('network', "")
% setdefault('network_ascii', "")

% setdefault('is_treechild', "-")
% setdefault('number_nodes', "-")
% setdefault('number_edges', "-")
% setdefault('number_hybrids', "-")
% setdefault('number_leafs', "-")
% setdefault('number_conflictive_nodes', "-")
% setdefault('number_removable_edges', "-")

<div id="main-pane" class="span8">
    <center>
      <div id="rendered-graph"> </div>
    </center>

    <div>
    % if network_ascii:
    <a class="btn download-network-buttons" target="_blank"
       download="phylonetwork_hard.csv"
       href="/network/{{cluster}}/hard/download" >Download <em>hard</em> as file</a>
    <legend>Cluster hardwired</legend>

    <pre>{{!network_hard}}</pre>
    % end
    </div>

    <div>
      <legend>Cluster softwired</legend>
      <div id="calc_soft_spinner">
       <p><i class="icon-spinner icon-spin"></i> Processing…</p>
      </div>
      <div id="cluster_soft_too_expensive" class="alert alert-error" style="display: none;">
        <p>Cannot calculate the <em>softwired</em> cluster because there are too many (up to {{subtrees}}) subtrees.</p>
      </div>

      <div id="cluster_softwired_field" style="display: none">
            <a class="btn download-network-buttons"
             download="phylonetwork_soft.csv" target="_blank"
                    href="/network/{{cluster}}/soft/download">Download <em>soft</em> as file</a>
        <pre id="cluster_softwired_field_pre"></pre>
      </div>
    </div>

    % if not is_treechild:
    <div>
    <legend>Tree-child families</legend>
       <div id="calc_families_spinner">
         <p><i class="icon-spinner icon-spin"></i> Processing…</p>
       </div>
       <div id="families_field" style="display: none">
          <pre id="families_field_pre"></pre>
       </div>
       <center>
          <div id="rendered-families"> </div>
       </center>

    </div>
    % end

</div>

<div class="span4">
 <legend>Graph legend</legend>
        <dl class="dl-horizontal">
          <dt>root</dt> <dd style="color: orange">orange node</dd>
          <dt>leafs</dt> <dd style="color: blue">blue node</dd>
          <dt>conflictive node</dt> <dd style="color: green">green node</dd>
          <dt>hybrid node</dt> <dd style="color: #7BFF74">light green node</dd>
          <dt>conflictive node</dt> <dd style="color: #FF77EB">pink node</dd>
          <dt>candidate edges</dt> <dd style="color: red">red edge</dd>
        </dl>
</div> <!-- span4 -->

<div class="span4">
  <legend>Network data</legend>
    <dl class="dl-horizontal">
      <dt>#nodes</dt> <dd>{{number_nodes}}</dd>
      <dt>#edges</dt> <dd>{{number_edges}}</dd>
      <dt>#leafs</dt> <dd>{{number_leafs}}</dd>
      <dt>#hybrids</dt> <dd>{{number_hybrids}}</dd>
      <dt>#hybrid degree</dt> <dd>{{hybridization_degree}}</dd>
      <dt>#subtrees</dt> <dd>{{subtrees}}</dd>
      <dt>is tree-child?</dt> <dd>
      % if is_treechild:
          <dd>Yes</dd>
      % else:
          <dd>No</d>
      % end
      <dt>#conflictive nodes</dt> <dd>{{number_conflictive_nodes}}</dd>
      <dt>#candidate edges</dt> <dd>{{number_removable_edges}}</dd>

      <div id="tree-child-message-yes" class="alert alert-success" style="display: none;">
      <div style="margin-left: -1em;">
        <dt>#tree-childs</dt> <dd id="tree-child-number">2</dd>
        </div>
      </div>

      <div id="tree-child-message-no" class="alert alert-error" style="display: none;">
        <dt>#tree-childs</dt> <dd>No</dd>
      </div>

    </dl>
</div> <!-- span4 -->


<script type="text/vnd.graphviz" id="network">
 {{!network_dot}};
</script>

<script src="/static/coffee/draw-network.js"></script>

<script>
  var soft_job_id = "{{soft_job_id}}";
  var soft_too_expensive = {{!soft_too_expensive}};
  var queue_id = "{{queue_key}}";
</script>

<script src="/static/coffee/remote-soft-calculation.js"></script>

% if not is_treechild:
<script>
  var families_job_id = "{{families_job_id}}";
</script>
<script src="/static/coffee/remote-treechild-calculation.js"></script>
% end

% rebase templates/base title=title
