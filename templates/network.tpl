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
    </dl>
</div> <!-- span4 -->


<script type="text/vnd.graphviz" id="network">
 {{!network_dot}};
</script>

<script src="/static/coffee/draw-network.js"></script>

% rebase templates/base title=title
