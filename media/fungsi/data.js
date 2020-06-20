$(function () {
    $("#btn_agregar_adjunto").click(function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-form").modal("show");
            },
            success: function (data) {
                $("#modal-form .modal-content").html(data.html_form);
            }
        });
    });

    $("#modal-form").on("submit", "#js_adjuntar_archivo_form", function () {
        var form = new FormData($(this)[0]);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.form_is_valid) {
                    alert("Archivo adjuntado");
                } else {
                    $("#modal-form .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });

});