function getValidationMessage(field) {
    const validity = field.validity;

    if (validity.valueMissing) {
        if (field.tagName === "SELECT") {
            return "Please select an option.";
        }

        return "Please fill out this field.";
    }

    if (validity.badInput) {
        return "Please enter a valid number.";
    }

    if (validity.rangeUnderflow) {
        return `Please enter a value greater than or equal to ${field.min}.`;
    }

    if (validity.rangeOverflow) {
        return `Please enter a value less than or equal to ${field.max}.`;
    }

    if (validity.stepMismatch) {
        if (field.name === "price_usd") {
            return "Please enter a price with at most two decimal places.";
        }

        return "Please enter a whole number.";
    }

    if (validity.tooLong) {
        return `Please use no more than ${field.maxLength} characters.`;
    }

    if (validity.typeMismatch) {
        return "Please enter a value in the required format.";
    }

    if (validity.patternMismatch) {
        return "Please match the requested format.";
    }

    return "Please check this field.";
}

document.addEventListener(
    "invalid",
    function (event) {
        const field = event.target;

        if (!(field instanceof HTMLInputElement) &&
            !(field instanceof HTMLSelectElement) &&
            !(field instanceof HTMLTextAreaElement)) {
            return;
        }

        field.setCustomValidity("");
        field.setCustomValidity(getValidationMessage(field));
    },
    true
);

function clearValidationMessage(event) {
    const field = event.target;

    if (typeof field.setCustomValidity === "function") {
        field.setCustomValidity("");
    }
}

document.addEventListener("input", clearValidationMessage);
document.addEventListener("change", clearValidationMessage);