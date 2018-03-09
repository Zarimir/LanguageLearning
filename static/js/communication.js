function elementify(elem) {
    /**
     * Multiple reactions could be activated for a single event.
     * A single deactivation affects all reactions to a given event.
     * Example usage:
     * elementify($("#id").wordsGetOne.activate(function (elementify, info) {});
     * elementify($("#id").wordsGetOne.deactivate();
     * @type {string}
     */
    var activate = "activate";
    var deactivate = "deactivate";
    var populate = "populate";
    var populateList = "populateList";
    var populateSelect = "populateSelect";
    var populateTable = "populateTable";
    elem = $(elem);
    function act(event, action) {
        var activateFunct = function (reaction) {
            elem.addClass(event);
            elem.on(event, function (event, response) {
                reaction(elem, response);
            });
        };
        var deactivateFunct = function () {
            elem.removeClass(event);
            elem.off(event);
        };
        var populateFunct = function (functionObj) {
            activateFunct(function (parent, info) {
                parent = $(parent);
                parent.empty();
                if (functionObj.hasOwnProperty("pre")) {
                    functionObj["pre"](parent);
                }
                if (functionObj.hasOwnProperty("population")) {
                    for (var i = 0; i < info.response.elements.length; i++) {
                        var element = info.response.elements[i];
                        functionObj["population"](parent, element);
                    }
                }
                if (functionObj.hasOwnProperty("post")) {
                    functinoObj["post"](parent);
                }
            });
        };
        var populateOneDimensionalLists = function (tag, functionObj) {
            var oldFunct = functionObj["population"];
            functionObj["population"] = function (parent, element) {
                var item = oldFunct(element);
                if (item.hasOwnProperty("child")) {
                    item.child.appendTo($("<" + tag + ">")).appendTo(parent);
                } else {
                    $("<" + tag + ">", item).appendTo(parent);
                }
            };
            populateFunct(functionObj);
        };
        var populateListFunct = function (functionObj) {
            populateOneDimensionalLists("li", functionObj);
        };
        var populateSelectFunct = function (functionObj) {
            populateOneDimensionalLists("option", functionObj);
        };
        var populateTableFunct = function (functionObj) {
            var oldFunct = functionObj["population"];
            functionObj["population"] = function (parent, element) {
                var row = $("<tr>");
                var cells = oldFunct(element);
                for (var i = 0; i < cells.length; i++) {
                    var cell = cells[i];
                    if (cell.hasOwnProperty("child")) {
                        cell.child.appendTo($("<td>")).appendTo(row);
                    } else {
                        $("<td>", cell).appendTo(row);
                    }
                }
                row.appendTo(parent);
            };
            populateFunct(functionObj);
        };

        switch(action) {
            case activate:
                return activateFunct;
            case deactivate:
                return deactivateFunct;
            case populate:
                return populateFunct;
            case populateList:
                return populateListFunct;
            case populateTable:
                return populateTableFunct;
            case populateSelect:
                return populateSelectFunct;
        }
    }
    return mapify($SCRIPT_EVENTS, [activate, deactivate, populate, populateList, populateTable, populateSelect], act);
}

function database() {
    /**
     * Example usage:
     * database().wordsGetOne(request);
     * @param event
     * @returns {Function}
     */
    var preProcess = function (event) {
        return function (requestRaw, callback) {
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
            processRequest(url, method, data, callback);
        }
    };
    return objectify(listify($SCRIPT_COLLECTIONS, $SCRIPT_METHODS, $SCRIPT_QUANTIFIERS), preProcess);
}

function processRequest(url, method, data, callback) {
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
    send(request, callback);
}

function send(request, callback) {
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
            if (callback) {
                callback();
            }
        },

        error: function (msg) {
            console.log(msg.status);
            console.log(msg.statusText);
        }
    });
}