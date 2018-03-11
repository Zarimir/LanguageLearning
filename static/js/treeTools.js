class Tree {
    constructor(elements) {
        this.elements = elements ? elements : [];
        this.element = {};
        this.roots = [];
        this.leaves = [];
        this.modified = [];
        this.relatives = [];
        this.memory = new Memory();
        Tree.parents = "parents";
        Tree.children = "children";
    }

    memorize() { this.memory.save() };
    remember(memory) { this.memory.load(memory) };

    memorizeElement(element) { return this.memory.push(element ? element : this.element); }
    rememberElement(memory) { this.element = this.memory.get(memory); }

    memorizeRelatives(relatives) { return this.memory.push(relatives ? relatives : this.relatives)}
    rememberRelatives(memory) { this.relatives = this.memory.get(memory); }

    modify(obj) { this.modified.push(obj ? obj : this.element); }

    save(element) { element ? this.saved = element : this.saved = this.element; }

    load(element) { element ? this.element = element : this.element = this.saved; }

    static HasRelatives(element, relatives) { return element[relatives].length > 0; }

    setRelatives(relatives) { this.relatives = this.element[relatives]; }

    getRelativeId(target) {
        /*
        this.relatives.filter(function (relative) {
            if relative._id === target._id;
        })?????????????????
        */
    }

    hasRelative(relatives, id) {
        this.setRelatives(relatives);
        return this.element[relatives].filter(function (relative) { return relative._id === id; } ).length > 0;
    }

    hasChild(id) { return this.hasRelative(Tree.children, id); }

    hasParent(id) { return this.hasRelative(Tree.parents, id); }

    hasRelatives(relatives) { return Tree.HasRelatives(this.element, relatives); }

    hasParents() { return this.hasRelatives(Tree.parents) }

    hasChildren() { return this.hasRelatives(Tree.children) }

    set(id) { this.element = this.get(id); }

    get(id) { return this.elements.filter(function (element) { return element._id === id })[0]; }

    collectElementsWithout(relatives) {
        return this.elements.filter(function (element) {
            return !Tree.HasRelatives(element, relatives);
        });
    }

    setRoots() { this.roots =  this.collectElementsWithout(Tree.parents); }

    setLeaves() { this.leaves = this.collectElementsWithout(Tree.children); }

    static IsSet(relative) { return typeof(relative) === "string"; }

    getUnset(relatives) { return this.element[relatives].filter(function (relative) { return Tree.IsSet(relative); }); }

    setRelatives(relatives) {
        var tree = new Tree(this.elements);
        var list = this.element[relatives];
        list.forEach(function (element, index) {
            Tree.IsSet(element) ? list[index] = tree.get(element) : null;
        });
    }

    setParents() { this.setRelatives(Tree.parents); }

    setChildren() { this.setRelatives(Tree.children); }

    setRelativesForAll(relatives) {
        var tree = new Tree(this.elements);
        tree.elements.forEach(function (element) {
            tree.load(element);
            tree.setRelatives(relatives);
        });
    }

    setParentsForAll() { this.setRelativesForAll(Tree.children); }

    setChildrenForAll() { this.setRelativesForAll(Tree.parents); }

    relate(subject_id, relation_to, object_id, relation_from) {
        var memory = this.memorizeElement();
        this.set(subject_id);
        if (!this.hasRelative(relation_to, object_id)) {
            this.element[relation_to].push(this.get(object_id));
            this.modify();
        }
        this.rememberElement(memory);
        this.load();
        relation_from ? this.relate(object_id, relation_from, subject_id) : null;
    }

    unrelate(subject_id, relation_to, object_id, relation_from) {
        var memory = this.memorizeElement();
        this.set(subject_id);
        if (this.hasRelative(relation_to, object_id)) {
            this.element[relation_to] = 0;
        }
        this.rememberElement(memory);
    }
}

Tree.test = function (param) {
    console.log(this);
    console.log(param);
}


var a = [
    {"_id": "1", "parents": [], "children":["5"]},
    {"_id": "2", "parents": [], "children":["6","7"]},
    {"_id": "3", "parents": [], "children":[]},
    {"_id": "4", "parents": [], "children":[]},
    {"_id": "5", "parents": ["1"], "children":["8"]},
    {"_id": "6", "parents": ["2"], "children":["9"]},
    {"_id": "7", "parents": ["2"], "children":["10", "11"]},
    {"_id": "8", "parents": ["5"], "children":[]},
    {"_id": "9", "parents": ["6"], "children":[]},
    {"_id": "10", "parents": ["7"], "children":["12"]},
    {"_id": "11", "parents": ["7"], "children":[]},
    {"_id": "12", "parents": ["10"], "children":[]}
];

var l = new Tree(a);
l.setRoots();
l.setLeaves();
l.relate("3", "children", "4", "parents");

var z = {"_id": "12", "parents": ["10"], "children":[]};

var s = {"_id": "2", "parents": [], "children":["6","7"]};

var elements = [
    {"_id": 1, "name": 1},
    {"_id": 2, "name": 1},
    {"_id": 3, "name": 1},
    {"_id": 4, "name": 1},
    {"_id": 5, "name": 2},
    {"_id": 5, "name": 3},
    {"_id": 5, "name": 4}
];

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

//setRelationRecursive(z, "parents", a);