function clearForm() {
    const form = document.getElementById("the-form");
    for (const input of form.getElementsByTagName("input")) {
        if (input.type !== "submit") {
            input.value = "";
            input.checked = false;
        }
    }
}

function populateExample1() {
    const form = document.getElementById("the-form");

    form.brand.value = "Audi";
    form.model.value = "A5";
    form.fuel.value = "Diesel";
    form.gearbox.value = "Automata";
    form.body.value = "Sedan";
    form.color.value = "Maro";
    form.drivetrain.value = "Fata";

    form.year.value = 2019;
    form.km.value = 155000;
    form.power.value = 190;
    form.cylinder_cap.value = 1998;
    form.doors.value = 4;
    form.consumption.value = 4.8;

    form.no_accident.checked = true;
    form.service_book.checked = true;
    form.particle_filter.checked = true;
    form.matriculated.checked = false;
    form.first_owner.checked = false;
}

function populateExample2() {
    const form = document.getElementById("the-form");

    form.brand.value = "Volkswagen";
    form.model.value = "Tiguan";
    form.fuel.value = "Diesel";
    form.gearbox.value = "Manuala";
    form.body.value = "SUV";
    form.color.value = "Gri";
    form.drivetrain.value = "4x4";

    form.year.value = 2018;
    form.km.value = 188820;
    form.power.value = 150;
    form.cylinder_cap.value = 1968;
    form.doors.value = 5;
    form.consumption.value = 6.7;

    form.no_accident.checked = false;
    form.service_book.checked = false;
    form.particle_filter.checked = true;
    form.matriculated.checked = true;
    form.first_owner.checked = true;
}

// Code to implement the photo preview functionality.
const photoPreview = document.getElementById("photo-preview");
document.getElementById("photo").onchange = function (_) {
    const [file] = document.getElementById("photo").files;
    if (file) {
        photoPreview.src = URL.createObjectURL(file);
        photoPreview.hidden = false;
    }
};
window.onload = function () {
    photoPreview.hidden = true;
};
