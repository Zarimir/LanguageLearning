elementify($("#languages")).languagesGetMany.populateTable({
    "population": (element) => [
            {
                "id": element._id,
                "html": element.language
            },
            {
                "child": $("<button>",
                    {
                        "onclick": "database().languagesDeleteOne({'_id': '" + element._id.toString() + "'});",
                        "html": "Delete"
                    })
            }
        ]
});

elementify($("#languages")).languagesDeleteOne.activate( () => database().languagesGetMany());

elementify($("#languages")).languagesPostOne.activate(() => database().languagesGetMany());

database().languagesGetMany();

enterClick($("#language"), $("#languageButton"));