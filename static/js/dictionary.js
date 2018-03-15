elementify(dictionary).languagesGetMany.populateSelect({
    "pre": addEmptyOption,
    "population": (element) => {
        return {
            "val": element._id,
            "html": element.language.substring(0, 1).toUpperCase() + element.language.substring(1).toLowerCase()
        };
    }
});

elementify(words).wordsPostOne.activate(() => database().wordsGetMany({"language_id": dictionary.val()}));

elementify(words).wordsDeleteOne.activate(() => database().wordsGetMany({"language_id": dictionary.val()}) );

database().languagesGetMany({}, () => selectOption(dictionary, languageID));

database().wordsGetMany({"language_id": dictionary.val()});

enterClick($("#word"), $("#wordButton"));



/*
var a = {
    "class": "slavic",
    "children": ["_id"]
};
var b = {
    "class": "west-slavic",
    "parent":"slavic",
    "languages": [1,2,3,4,5,6]
};
var b = {
    "class": "south-slavic",
    "parent":"slavic",
    "languages": [1,2,3,4,5,6]
};
var b = {"class": "east-slavic", "languages": [1,2,3,4,5,6]};
var c = {
    "slavic": {
        "west": [
            "polish",
            "czech",
            "slovak"
        ],
        "east": [
            "russian",
            "belorussian",
            "ukrainian"
        ],
        "south": [
            "bulgarian",
            "macedonian",
            "croatian",
            "serbian",
            "bosnian",
            "montenegrin"
        ]
    },
    "germanic": {
        "west": [
            "english",
            "german",
            "dutch"
        ],
        "north": [
            "icelandic",
            "norwegian",
            "danish",
            "swedish"
        ]
    },
    "romance": [
        "italian",
        "french",
        "spanish",
        "portuguese"
    ],
    "semitic": [
        "hebrew"
    ],
    "japonic": [
        "japanese"
    ]
};
*/