function enterClick(element, clickable) {
    /**
     * Makes a clickable object respond to ENTER key.
     */
    element.keypress(function (e) {
        var key = e.which;
        if (key === 13) {
            clickable.click();
        }
    });
}

function collectFormFields() {
    /**
     * Collects all fields from a form and validates them.
     * @type {{}}
     */
    var extraction = {};
    for (var i = 0; i < arguments.length; i++) {
        var form = $(arguments[i]);
        if (!form[0].checkValidity()) {
            form.find("input[type='submit']").first().click();
        } else {
            var fields = form.find("input, select");
            fields.each(function (index, field) {
                field = $(field);
                var name = field.attr("name");
                if (name) {
                    extraction[name] = field.val();
                }
            });
        }
    }
    return extraction;
}

function selectOption(select, optionValue, obj) {
    /**
     * Selects an option with value optionValue from a select element and deselects
     * all other elements. IF there is no such option, it selects the default option.
     * @type {*|jQuery|HTMLElement}
     */
    select = $(select);
    var optionEmpty = select.find(".optionEmpty").first();
    var found = false;
    select.find("option").each(function (index, option) {
       option = $(option);
       if (optionValue && option.val() === optionValue) {
           found = true;
           callObj(obj, "selected", option, optionEmpty);
           option.prop("selected", true);
       } else {
           callObj(obj, "unselected", option, optionEmpty);
           option.prop("selected", false);
       }
    });
    if (!found) {
        callObj(obj, "empty", optionEmpty);
        optionEmpty.prop("selected", true);
    }
    select.change();
}

function disableOption(select, optionValue) {
    select = $(select);
    var optionEmpty = select.find(".optionEmpty").first();
    select.find("option").each(function (index, option) {
        option = $(option);
        if (option.val() === optionValue) {
            if (option.prop("selected")) {
                option.prop("selected", false);
                optionEmpty.prop("selected", true);
            }
            option.prop("disabled", true);
        } else {
            option.prop("disabled", false);
        }
    });
}

function addSubmitToForm(form, value) {
    var submit = $("<input>", {"type": "submit"});
    if (value) {
        submit.val(value);
    } else {
        submit.prop("hidden", true);
    }
    submit.appendTo(form);
    return submit;
}

function addEmptyOption(select) {
    $("<option>",{
        "class": "optionEmpty",
        "disabled": true,
        "hidden": true,
        "selected": true
    }).appendTo(select);
}