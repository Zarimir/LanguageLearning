function element(elem) {
    /**
     * Multiple reactions could be activated for a single event.
     * A single deactivation affects all reactions to a given event.
     * Example usage:
     * element($("#id").wordsGetOne.activate(function (element, info) {});
     * element($("#id").wordsGetOne.deactivate();
     * @type {string}
     */
    var activate = "activate";
    var deactivate = "deactivate";
    function act(event, action) {
        if (action === activate) {
            return function (reaction) {
                elem.addClass(event);
                elem.on(event, function (event, response) {
                   reaction(elem, response);
                });
            }
        } else if (action === deactivate) {
            return function () {
                elem.removeClass(event);
                elem.off(event);
            };
        }
    }
    return mapify($SCRIPT_EVENTS, [activate, deactivate], act)
}

function database() {
    /**
     * Example usage:
     * database().wordsGetOne(request);
     * @param event
     * @returns {Function}
     */
    var preProcess = function (event) {
        return function (requestRaw) {
            var data = Object.assign({}, requestRaw);
            data.event = event;
            var url = $SCRIPT_REST + splitOnUpperCase(event)[0];
            var method = splitOnUpperCase(event)[1].toUpperCase();
            /*
            console.log("URL: " + url.toString());
            console.log("METHOD: " + method.toString());
            console.log("EVENT: " + event.toString());
            console.log("REQUEST: ");
            console.log(data);
            */
            processRequest(url, method, data);
        }
    };
    return objectify(listify($SCRIPT_COLLECTIONS, $SCRIPT_METHODS, $SCRIPT_QUANTIFIERS), preProcess);
}

function processRequest(url, method, data) {
    /**
     * Puts the data in the url as parameters for get requests.
     * JSONIFIES the data for all other requests
     * @type {{}}
     */
    var request = {};
    request.method = method;
    request.url = url;
    request.dataRaw = Object.assign({}, data);
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
    /**
     * Sends the request's data to the server.
     * Receives server response.
     * Processes the request and the response.
     */
    $.ajax({
        url: request.url,
        method: request.method,
        contentType: request.contentType,
        data: request.data,
        success: function (response) {
            console.log();
            console.log("request");
            console.log(request);
            console.log("response:");
            console.log(response);
            var info = {"request": request, "response": response};
            $("." + request.dataRaw.event).trigger(request.dataRaw.event, info);
        },

        error: function (msg) {
            console.log(msg.status);
            console.log(msg.statusText);
        }
    });
}