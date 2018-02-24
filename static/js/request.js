function send(callback, request) {
    console.log(callback);
    console.log(request);
    $.ajax({
        url: "/",
        method: "POST",
        data: JSON.stringify(request),
        contentType: 'application/json; charset=utf-8',
        dataType: "json",
        success: function (response) {
            console.log();
            console.log("request:");
            console.log(request);
            console.log("response:");
            console.log(response);
        }
    });
}
