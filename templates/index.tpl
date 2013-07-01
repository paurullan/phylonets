% setdefault('error', "")

<!-- venim d'un row i tenim 12 spans -->

<div class="span3">
    <center>
    <h5 class="text-info">Examples</h5>
    <div class="btn-toolbar">
        <div class="btn-group-vertical">
            % for name, location in examples:
            <a href="cluster/{{location}}" class="btn btn-option">{{name}}</a>
            % end
        </div>
    </div>
    </center>
</div>

<div class="span9">
     % if error:
     <div id="form_error" style="" class="alert alert-error">
       <p>{{error}}</p>
     </div>
     % end
    <p class="lead">There are many ways you can submit a network; choose the one that most fits you.</p>

    <p>Send the networks writting into the fields</p>
    <form action="/input/cluster/" method="post">
        <fieldset>
        <button type="submit" class="btn index-submit-button" tabindex="2">Process cluster</button>
        <legend>Clusters</legend>
            <span class="help-block">Cluster list from items, seppared by parens and commas.</span>
            <input name="clusters" required="true" class="span9" type="text" placeholder="(1, 2), (3, 4)" tabindex="1">
        </label>
        </fieldset>
    </form>

    <form action="/input/enewick/" method="post">
        <fieldset>
        <button type="submit" class="btn index-submit-button" tabindex="4">eNewick</button>
        <legend>eNewick</legend>
            <span class="help-block">Input an <a href="/help#intro-enewick">eNewick format graph</a>.</span>
            <input class="span9" required="true" type="text" name="enewick" placeholder="((4, 5#1)2, (#1, 6)3);" tabindex="3">
        </label>
        </fieldset>
    </form>

    <form action="/input/upload/" method="post" enctype="multipart/form-data">
        <fieldset>

        <legend>Load from file</legend>
         <label class="radio">
           <input type="radio" name="optionsRadios" id="optionsRadios1" value="cluster" checked>
           cluster list
         </label>
         <label class="radio">
           <input type="radio" name="optionsRadios" id="optionsRadios2" value="enewick">
           eNewick
         </label>
        </fieldset>

        <fieldset>
        <button type="submit" style="float: right"
                class="btn" tabindex="21">
                Upload and process</button>
        <input name="data" required="true" type="file" tabindex="22">
        </fieldset>

    </form>

    </div> <!-- end tab-content -->

</div>
% rebase templates/base
