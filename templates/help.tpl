<!-- venim d'un row i tenim 12 spans -->
% setdefault('title', "Help section")

<h3 id="intro-enewick">The eNewick format</h3>

The extended Newick format, or <em>eNewick</em>, is a complete notation for graph representation used for phylogenetic networks. As an extension of Newick, the hybrid nodes are specified as:

<pre style="width: 25em">[label]#[type]tag[:branch_length]</pre>


<div class="span4">
A simple net would be:
<pre>(1, (2), #h), (#h, 3));</pre>
</div>
<div class="span4">
<img src="/static/img/enewick.svg" widht="20em" height="20em" />
</div>

<div class="span11">
Related links:

<ul>
<li><a href="http://en.wikipedia.org/wiki/Newick_format">Newick page in Wikipedia</a></li>
<li><a href="http://dmi.uib.es/~gcardona/BioInfo/enewick.html">Detailed use of eNewick</a></li>
<li><a href="http://www.biomedcentral.com/1471-2105/9/532/">Original article for eNewick</a></li>
</ul>
</div>
% rebase templates/base title=title
