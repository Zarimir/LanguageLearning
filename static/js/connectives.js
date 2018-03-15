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
    iterate(arguments, (argument) => currentArgs.push(argument));
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
        return typeof(callback) === "function" ? call(callback, callbackArgs) : null;
    } else {
        return null;
    }
}