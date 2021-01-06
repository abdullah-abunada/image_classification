/*  Wizard */
jQuery(function ($) {
    "use strict";
    $("#wizard_container").wizard({
        stepsWrapper: "#wrapped",
        submit: ".submit",
        unidirectional: false,
        beforeSelect: function (event, state) {
            if ($('input#website').val().length != 0) {
                return false;
            }
            if (!state.isMovingForward)
                return true;
            var inputs = $(this).wizard('state').step.find(':input');
            return !inputs.length || !!inputs.valid();
        }
    }).validate({
        errorPlacement: function (error, element) {
            if (element.is(':radio') || element.is(':checkbox')) {
                error.insertBefore(element.next());
            } else {
                error.insertAfter(element);
            }
        }
    });
    //  progress bar
    $("#progressbar").progressbar();
    $("#wizard_container").wizard({
        afterSelect: function (event, state) {
            $("#progressbar").progressbar("value", state.percentComplete);
            $("#location").text("" + state.stepsComplete + " of " + state.stepsPossible + " completed");
        }
    });
});

$("#wizard_container").wizard({
    transitions: {
        branchtype: function ($step, action) {
            var branch = $step.find(":checked").val();
            if (!branch) {
                $("form").valid();
            }
            return branch;
        }
    }
});

/* File upload validate size and file type - For details: https://github.com/snyderp/jquery.validate.file*/
$("form#wrapped")
    .validate({
        rules: {
            file_upload: {
                fileType: {
                    types: ["image/jpeg", "image/jpg"]
                },
                maxFileSize: {
                    "unit": "MB",
                    "size": 2
                },
                minFileSize: {
                    "unit": "KB",
                    "size": "2"
                }
            }
        }
    });

// bind submit handler to form
$("form#wrapped").on('submit', function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    $('#flower_type').val('')
    let form = $(this);
    let fd = new FormData();
    let files = $('#file_upload')[0].files;
    let model = $("input[name='model']:checked").val();
    fd.append('file', files[0]);
    fd.append('model', model);
    let url = form.attr('action');
    $.ajax({
        type: "POST",
        url: url,
        contentType: false,
        processData: false,
        data: fd, // serializes the form's elements.
        success: function (data) {
            $('#flower_type').val(data.result)
            $('#loader_form').hide()
            $('#prediction_results').modal({ show: true})
        },
        error: function (data) {
            $('#loader_form').hide()
        }
    });
});

// Input name and email value
function getVals(formControl, controlType) {
    switch (controlType) {

        case 'name_field':
            // Get the value for input
            var value = $(formControl).val();
            $("#name_field").text(value);
            break;

        case 'email_field':
            // Get the value for input
            var value = $(formControl).val();
            $("#email_field").text(value);
            break;
    }
}

// display selected image in results modal
function readURL(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            $('#sample_image')
                .attr('src', e.target.result)
                .width(150)
                .height(150);
        };
        reader.readAsDataURL(input.files[0]);
    }
}