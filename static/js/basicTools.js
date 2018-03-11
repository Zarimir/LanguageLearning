function call(funct, list) { return funct.apply(this, list); }

function callObj(obj, trigger, params) {
    if (obj && obj.hasOwnProperty(trigger)) {
        var args = [];
        iterate(arguments, function (argument, index) {
            if (index > 1) { args.push(argument); }
        });
        return call(obj[trigger], args);
    }
    return null;
}


function iterate(arguments, callback) {
    var result = [];
    for (var i = 0; i < arguments.length; i++) {
        var element = arguments[i];
        callback(element, i) ? result.push(element) : null;
    }
    return result;
}

function splitOnUpperCase(string) {
    /**
     * Example usage:
     * "" -> []
     * "a" -> ["a"]
     * "aBbbb" -> ["a", "Bbbb"]
     * "aBbCccD" -> ["a", "Bb", "Ccc", "D"]
     * @type {Array}
     */
    var split = [];
    var index = 0;
    for (var i = 0; i < string.length; i++) {
        var code = string.charCodeAt(i);
        if ("A".charCodeAt(0) <= code && code <= "Z".charCodeAt(0)) {
            split.push(string.substring(index, i));
            index = i;
        }
    }
    split.push(string.substring(index));
    return split;
}

function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase();
}