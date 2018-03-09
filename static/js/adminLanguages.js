elementify($("#languages")).languagesGetMany.populateTable(function (element) {
   return [{
           "id": element._id,
           "html": element.language
       },
       {
           "child": $("<button>", {
               "onclick": "database().languagesDeleteOne({'_id': '" + element._id.toString() + "'});",
                "html": "Delete"
           })
       }
   ]
});

elementify($("#languages")).languagesDeleteOne.activate(function () {
   database().languagesGetMany();
});

elementify($("#languages")).languagesPostOne.activate(function () {
   database().languagesGetMany();
});

database().languagesGetMany();

enterClick($("#language"), $("#languageButton"));