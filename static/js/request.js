function methods(callback) {
    return {
        "get": {
            "one": callback("GET", "ONE"),
            "many": callback("GET", "MANY")
        },
        "post": callback("POST"),
        "put": callback("PUT"),
        "delete": callback("DELETE")
    };
}
function collections(callback) {
    obj = {};
    $SCRIPT_COLLECTIONS.forEach(function (item) {
       obj[item] = callback(item);
    });
    return obj;
}

var obj = {};
$SCRIPT_METHODS.forEach(function (method) {
   if (method.hasOwnProperty("param")) {
       method.param.forEach(function (param) {
           obj[method + param.charAt(0).toUpperCase() + param.slice(1)] = method + "-" + param
       });
   }
});

function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}
function database() {
    /*
    Example usage:
    database().words.get.one(request);
     */
    var select = function (collection) {
        var act = function (method, parameter) {
            return function (requestRaw) {
                parameter = (parameter) ? parameter : "";
                var url = $SCRIPT_REST + collection;
                var action = collection + capitalizeFirst(method) + capitalizeFirst(parameter);
                processRequest(url, method, action, requestRaw);
                /*
                console.log("url: " + url);
                console.log("method: " + method);
                console.log("action: " + action);
                console.log("request: ");
                console.log(requestRaw);
                */
            }
        };
        return methods(act);
    };
    return collections(select);
}

function processRequest(url, method, acttion, requestRaw) {
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
            console.log(msg.status);
            console.log(msg.statusText);
        }
    });
}

function processResponse (response) {
    $(".languages-get").trigger("languages-get", response);
}
