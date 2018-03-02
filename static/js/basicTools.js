/*
function constructObjects(listA, listB) {
    /**
     * Example result:
     * listA = ['a','b','c'];
     * listB = ['1','2','3'];
     * result = [];
     * @type {Array}
     */
/*
    var objs = [];
    for (var a = 0; a < listA.length; a++) {
        var key = listA[a];
        var values = [];
        for (var b = 0; b < listB.length; b++) {
            var value = listB[b];
            values.push(value);
        }
        var obj = {};
        obj[key] = values;
        objs.push(obj);
    }
    return objs
}
*/


function listify() {
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

function objectify(list, callback) {
    /**
     * Returns an object where the keys are
     * the list's elements and the values are the
     * callback with the key as an argument.
     *
     * Example usage:
     * var list = ['a','b','c'];
     * var callback = function (item) {...};
     * result = {
     *    'a': callback('a'),
     *    'b': callback('b'),
     *    'c': callback('c')
     * }
     * @type {{}}
     */
    var obj = {};
    list.forEach(function (item) {
       obj[item] = callback(item);
    });
    return obj;
}

function mapify(listA, listB, callback) {
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
    var objA = {};
    for (var i = 0; i < listA.length; i++) {
        var keyA = listA[i];
        var objB = {};
        for (var j = 0; j < listB.length; j++) {
            var keyB = listB[j];
            objB[keyB] = callback(keyA, keyB);
        }
        objA[keyA] = objB;
    }
    return objA;
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