function constructObjects(listA, listB) {
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


var events = ['a', 'b','c'];
var events = [$METHODS]
function constructEvents() {
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

var collections = ["words", "users", "languages", "synonyms"];
var methods = ["get", "post", "put", "delete"];
var quantity = ["one", "many"];




function splitOnUpperCase(string) {
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