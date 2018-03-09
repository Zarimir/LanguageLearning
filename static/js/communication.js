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
        var populateFunct = function (formatParent) {
            activateFunct(function (parent, info) {
                parent.empty();
                for (var i = 0; i < info.response.elements.length; i++) {
                    var element = info.response.elements[i];
                    formatParent(parent, element);
                }
            });
        };
        var populateOneDimensionalLists = function (tag, formatItem) {
            populateFunct(function (parent, element) {
                var item = formatItem(element);
                if (item.hasOwnProperty("child")) {
                    item.child.appendTo($("<" + tag + ">")).appendTo(parent);
                } else {
                    $("<" + tag + ">", item).appendTo(parent);
                }
            });
        };
        var populateListFunct = function (formatItem) {
            populateOneDimensionalLists("li", formatItem);
        };
        var populateSelectFunct = function (formatItem) {
            populateOneDimensionalLists("option", formatItem);
        };
        var populateTableFunct = function (formatRow) {
            populateFunct(function (parent, element) {
                var row = $("<tr>");
                var cells = formatRow(element);
                for (var i = 0; i < cells.length; i++) {
                    var cell = cells[i];
                    if (cell.hasOwnProperty("child")) {
                        cell.child.appendTo($("<td>")).appendTo(row);
                    } else {
                        $("<td>", cell).appendTo(row);
                    }
                }
                row.appendTo(parent);
            });
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