var words = $("#words");
var dictionary = $("#dictionary");


elementify(dictionary).languagesGetMany.populateSelect({
    "pre": addEmptyOption,
    "population": function (element) {
        return {
            "val": element._id,
            "html": element.language.substring(0,1).toUpperCase() + element.language.substring(1).toLowerCase()
        };
    }
});

elementify(words).wordsGetMany.populateList({
    "population": function (element) {
        return {
            "id": element._id,
            "html": element.word
        };
    }
});

elementify(words).wordsPostOne.activate(function () {
    database().wordsGetMany({"language_id": dictionary.val()});
});

elementify(words).wordsDeleteOne.activate(function () {
    database().wordsGetMany({"language_id": dictionary.val()});
});

database().languagesGetMany({}, function () { selectOption(dictionary, languageId); });

database().wordsGetMany({"language_id": dictionary.val()});
enterClick($("#word"), $("#wordButton"));
