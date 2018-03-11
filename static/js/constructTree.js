var a = [
    {"_id": 1, "parent": null, "children":[5]},
    {"_id": 2, "parent": null, "children":[6,7]},
    {"_id": 3, "parent": null, "children":[]},
    {"_id": 4, "parent": null, "children":[]},
    {"_id": 5, "parent": "1", "children":[8]},
    {"_id": 6, "parent": "2", "children":[9]},
    {"_id": 7, "parent": "2", "children":[10, 11]},
    {"_id": 8, "parent": "5", "children":[]},
    {"_id": 9, "parent": "6", "children":[]},
    {"_id": 10, "parent": "7", "children":[12]},
    {"_id": 11, "parent": "7", "children":[]},
    {"_id": 12, "parent": "10", "children":[]}
];

function tree(data) {
    //$("<ul>")
    var roots = [];
    var elements = [];
    data.forEach(function (element) {
        (element.parent === null) ? roots.push(element) : elements.push(element);
    });
    roots.forEach(function (root) {
        setChildrenRecursive(root, elements);
    });
    return roots;
}

var elements = [
    {"_id": 1, "name": 1},
    {"_id": 2, "name": 1},
    {"_id": 3, "name": 1},
    {"_id": 4, "name": 1},
    {"_id": 5, "name": 2},
    {"_id": 5, "name": 3},
    {"_id": 5, "name": 4}
];
function popID(elements, id) {
    var i = 0;
    while (i < elements.length) {
        var element = elements[i];
        if (element._id === id) {
            elements.splice(i, 1);
            return (element);
        }
        i++;
    }
    return null;
}

function setParent(element, elements) {
    if (element.parent) {
        element.parent = popID(elements, element.parent);
    }
}

function setParentRecursive(element, elements) {
    setParent(element, elements);
    (element.parent) ? setParentRecursive(element.parent) : null;
}

function setChildren(element, elements) {
    if (element.children.length) {
        element.children.forEach(function (childID, index) {
            element.children[index] = popID(elements,childID);
        });
    }
}

function setChildrenRecursive(element, elements) {
    setChildren(element, elements);
    element.children.forEach(function (child) {
       setChildrenRecursive(child, elements);
    });
}

function branchTree(obj) {
    var masterItem = $("<li>", {
        "html": obj.classification
    });
    if (obj.children.length) {
        var list = $("<ul>").appendTo(masterItem);
        for (var i = 0; i < obj.children.length; i++) {
            var child = obj.children[i];
            branchTree(child).appendTo(list);
        }
    }
    return masterItem;
}

