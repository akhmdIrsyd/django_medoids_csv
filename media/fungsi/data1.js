$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-data .modal-content").html("");
                $("#modal-data").modal("show");
            },
            success: function (data) {
                $("#modal-data .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var formData = new FormData($(this)[0]);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data1: form.serialize(),
            data: formData,
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#data-table tbody").html(data.html_data_list);
                    $("#modal-data").modal("hide");
                    window.location.href = response.redirect;
                }
                else {
                    $("#modal-data .modal-content").html(data.html_form);
                    window.location.href = response.redirect;
                }
            }
        });
        return false;
    };

    var upload = function () {
        var formData = new FormData(this);
        $.ajax({
            data: formData,
        });
        return false;
    };



    /* Binding */

    // Create book
    $(".js-create-data").click(loadForm);
    $("#modal-data").on("submit", ".js-data-create-form", saveForm);

    // Update book
    $("#data-table").on("click", ".js-update-data", loadForm);
    $("#modal-data").on("submit", ".js-data-update-form", saveForm);

    // Delete book
    $("#data-table").on("click", ".js-data-book", loadForm);
    $("#modal-data").on("submit", ".js-data-delete-form", saveForm);

});