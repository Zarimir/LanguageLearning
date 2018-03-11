function permutate() {
    /**
     * Creates a list of all permutations of the input;
     * the order of the list arguments determines the
     * permutation positions in the result.
     *
     * Example usage:
     * var a = ['a','b','c']; // 1st position
     * var b = ['get']; // 2nd position
     * var c = ['1','2','3'] //3rd position
     * result = [
     * 'aGet1', 'aGet2', 'aGet3',
     * 'bGet1', 'bGet2', 'bGet3',
     * 'cGet1', 'cGet2', 'cGet3'
     * ];
     * @type {Array}
     */
    var permutations = [];
    for (var i = 0; i < arguments.length; i++) {
        var list = arguments[i];
        var temp = [];
        for (var j = 0; j < list.length; j++) {
            var arg = list[j];
            if (i === 0) {
                permutations.push([arg.toLowerCase()]);
            } else {
                for (var k = 0; k < permutations.length; k++) {
                    var permutation = permutations[k];
                    permutation += arg.charAt(0).toUpperCase() + arg.substring(1).toLowerCase();
                    temp.push(permutation);
                }
            }
        }
        permutations = (i > 0) ? temp: permutations;
    }
    return permutations;
}

function iterateVarArg(arguments, callback) {
    for (var i = 0; i < arguments.length; i++) {
        callback(arguments[i]);
    }
}

function mapListsToCallback() {
    /**
     * Example usage:
     * listA = ["a","b","c"];
     * listB = ["1","2"];
     * result = {
     *   "a": {
     *      "1": callback("a", "1"),
     *      "2": callback("a", "2")
     *   },
     *   "b": {
     *      "1": callback("b", "1"),
     *      "2": callback("b", "2")
     *   },
     *   "c": {
     *      "1": callback("c", "1"),
     *      "2": callback("c", "2")
     *   }
     * }
     * @type {{}}
     */
    function listLast(list, replacement) {
        var index = list.length - 1;
        !(replacement === undefined) ? list[index] = replacement : null;
        return list[index];
    }
    function recurseArgs(currentArgs, arg) {
        var callbackArgs = listLast(currentArgs).slice();
        var recursiveArgs = currentArgs.slice();
        listLast(recursiveArgs, callbackArgs);
        recursiveArgs.splice(0, 1);
        callbackArgs.push(arg);
        return recursiveArgs;
    }
    var currentArgs = [];
    iterateVarArg(arguments, function (argument) { currentArgs.push(argument); });
    var length = currentArgs.length;
    var callbackArgs = arguments[length - 1];
    !$.isArray(callbackArgs) ? currentArgs.push([]): null;
    length = currentArgs.length;
    if (length > 2) {
        var obj = {};
        currentArgs[0].forEach(function (arg) {
            var recursiveArgs = recurseArgs(currentArgs, arg);
            obj[arg] = mapListsToCallback.apply(this, recursiveArgs)
        });
        return obj;
    } else if (length === 2) {
        var callback = currentArgs[0];
        return typeof(callback) === "function" ? callback.apply(this, callbackArgs) : null;
    } else {
        return null;
    }
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

function enterClick(element, clickable) {
    element.keypress(function (e) {
        var key = e.which;
        if (key === 13) {
            clickable.click();
        }
    });
}

function extractInput() {
    var extraction = {};
    for (var i = 0; i < arguments.length; i++) {
        var form = $(arguments[i]);
        if (!form[0].checkValidity()) {
            form.find("input[type='submit']").first().click();
        } else {
            var fields = form.find("input, select");
            fields.each(function (index, field) {
                field = $(field);
                var name = field.attr("name");
                if (name) {
                    extraction[name] = field.val();
                }
            });
        }
    }
    return extraction;
}

function selectOption(select, optionValue) {
    select = $(select);
    var optionEmpty = select.find(".optionEmpty").first();
    var found = false;
    select.find("option").each(function (index, option) {
       option = $(option);
       option.prop("selected", false);
       if (option.val() === optionValue) {
           found = true;
           option.prop("selected", true);
       }
    });
    if (!found) {
        optionEmpty.prop("selected", true)
    }
    select.change();
}

function updateSelect(select, optionValue) {
    select = $(select);
    var optionEmpty = select.find(".optionEmpty").first();
    select.find("option").each(function (index, option) {
        option = $(option);
        if (option.val() === optionValue) {
            if (option.prop("selected")) {
                option.prop("selected", false);
                optionEmpty.prop("selected", true);
            }
            option.prop("disabled", true);
        } else {
            option.prop("disabled", false);
        }
    });
}

function addSubmit(form, value) {
    var submit = $("<input>", {"type": "submit"});
    if (value) {
        submit.val(value);
    } else {
        submit.prop("hidden", true);
    }
    submit.appendTo(form);
    return submit;
}

function addEmptyOption(select) {
    $("<option>",{
        "class": "optionEmpty",
        "disabled": true,
        "hidden": true,
        "selected": true
    }).appendTo(select);
}

function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase();
}