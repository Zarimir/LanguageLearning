var words = $("#words");
var language = $("#language");

elementify(language).languagesGetMany.populateSelect(function (element) {
    return {
        "val": element._id,
        "html": element.language.substring(0,1).toUpperCase() + element.language.substring(1).toLowerCase()
    };
});

elementify(words).wordsGetMany.populateTable(function (element) {
    return [
        {
            "id": element._id,
            "html": element.word
        },
        {
            "child": $("<button>", {
                "onclick": "database().wordsDeleteOne({'_id': '" + element._id.toString() + "'}); database().wordsGetMany({'language_id': '" + language.val() + "'})",
                "html": "Delete"
            })
        }
    ];
});

elementify(words).wordsPostOne.activate(function () {
    database().wordsGetMany({"language_id": language.val()});
});

elementify(words).wordsDeleteOne.activate(function () {
    database().wordsGetMany({"language_id": language.val()});
});

database().languagesGetMany();
database().wordsGetMany({"language_id": language.val()});
enterClick($("#word"), $("#wordButton"));