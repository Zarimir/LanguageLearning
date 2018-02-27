function database() {
    /*
    Example usage:
    database().words.get(request);
     */
    var base = $SCRIPT_ROOT + "rest/";
    var select = function (url) {
        var act = function (method) {
            return function (requestRaw) {
                processRequest(url, method, requestRaw);
            }
        };
        return {
            "get": act("GET"),
            "post": act("POST"),
            "put": act("PUT"),
            "delete": act("DELETE")
        };
    };
    return {
        "words": select(base + "words"),
        "languages": select(base + "languages")
    };
}

function processRequest(url, method, requestRaw) {
    var request = {};
    var data = Object.assign({}, requestRaw);
    request.method = method;
    request.url = url;
    delete data.url;
    if (method === "GET") {
        request.contentType = "application/x-www-form-urlencoded; charset=UTF-8";
        parameters = jQuery.param(data);
        request.url = (parameters) ? request.url + "?" + parameters : request.url;
    } else {
        var parameters;
        request.contentType = "application/json; charset=utf-8";
        request.data = JSON.stringify(data);
    }
    send(request);
}

function send(request) {
    $.ajax({
        url: request.url,
        method: request.method,
        contentType: request.contentType,
        data: request.data,
        success: function (response) {
            console.log();
            console.log("request:");
            console.log(request);
            console.log("response:");
            console.log(response);
            processResponse(response);
        },
        error: function (msg) {
            alert(msg);
        }
    });
}

function processResponse (response) {
    $(".languages-get").trigger("languages-get", response);
}
