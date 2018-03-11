class Memory {
    constructor() { this.heap = []; }

    toString() { return this.heap.toString(); }

    save() { return this.heap.length; }

    load(length) { this.pop(this.heap.length - length); return this; }

    get(length) { return this.heap[length - 1]; }

    push() { var heap = this.heap; iterate(arguments, function (argument) { heap.push(argument); }); return this.save() }

    pop(count) {
        var value = this.heap.pop();
        if (count === undefined) {
            return this.value;
        } else if (count > 1) {
            return this.pop(count - 1).concat([value]);
        } else {
            return [value];
        }
    }
}

/*
var memory = new Memory();
memory.push(5, 7, 4, 3, 2, 1, 2, 3);
var ints = memory.save();
memory.push("hello");
memory.push("hmm");
memory.push("this", "is", " a", " sentence");
*/