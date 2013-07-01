<!DOCTYPE html>
<html>
    <head>
        <title>Phylonets web</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="/static/css/cerulean/bootstrap.min.css" rel="stylesheet" media="screen">
        <link href="/static/css/bootstrap-responsive.min.css" rel="stylesheet" media="screen">
        <link href="/static/css/font-awesome.min.css" rel="stylesheet" media="screen">
        <link href="/static/sass/phylonetwork.css" rel="stylesheet" media="screen">
        <link rel="shortcut icon" href="static/img/favicon.ico">
    </head>

    <body>
    <script src="/static/js/jquery-1.9.1.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/bootstrap-filestyle-0.1.0.min.js"></script>
    <script src="/static/js/viz.js"></script>

    <div class="container-fluid">

        <div class="masthead">
            <ul class="nav nav-pills pull-right">
                <li><a href="/help">Help</a></li>
                <li><a href="/about">About</a></li>
            </ul>
            <h3 class="muted"><a href="/">Phylonets web</a></h3>
        </div> <!-- /masthead -->

        <div class="row-fluid">
          <noscript>
            <h1 id="noscript">Please, enable JavaScript to visit correctly this site.</h1>
          </noscript>


            <div class="span12">
                % setdefault('title', "Analyzing phylogenetic networks")
                <h2>{{title}}</h2>
            </div>
        </div> <!-- /row -->

        <div class="row-fluid">
            %include
        </div> <!-- /row -->

      <hr>
      <div class="footer">
        <div class="container-fluid">
          <p><a href="/about">CC SA + BSA + Affero</a>, <a href="http://rullan.cat">Pau Ruŀlan Ferragut</a></p>
        </div>
      </div>

    </div> <!-- /container -->

    <!-- local scripts -->
    <script src="/static/coffee/phylonetwork-web-assets.js"></script>

    </body>
</html>
