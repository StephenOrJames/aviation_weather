$(document).foundation();

$(document).ready(function () {
    // For the sandbox
    if ($("#sandbox").length > 0) {
        var qAction = $("select[name=action]");
        var qType = $("select[name=type]");
        var qSubtype = $("select[name=subtype]");
        var qText = $("input[name=text]");
        var qResult = $("#result");

        // Hide except action until needed
        $("label").hide();
        qAction.parent().show();

        // Show the next prompt if the action was selected
        qAction.change(function () {
            if (this.value) {
                // Show only the relevant optgroup
                qType.find("optgroup").hide();
                qType.find("optgroup[label=" + this.value + "]").show();
                qType.parent().show();
            }
        });

        qType.change(function () {
            if (this.value) {
                if (this.value === "component") {
                    // Get the subtype (component type)
                    qSubtype.parent().show();
                } else {
                    qSubtype.parent().hide();
                    qText.parent().show();
                }
            }
        });

        qSubtype.change(function () {
            if (this.value) {
                qText.parent().show();
            }
        });

        $("form").submit(function (e) {
            e.preventDefault();

            var url = "api/" + qAction.val() + "/" + qType.val();
            if (qType.val() === "component") {
                url += "/" + qSubtype.val();
            }
            url += "/" + qText.val();

            $.getJSON(url)
                .success(function (obj) {
                    qResult.text(
                        JSON.stringify(obj, null, 2)
                    );
                })
                .fail(function () {
                    alert("Your query failed.");
                })
            ;
        });
    }
});
