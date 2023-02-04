function populateExample1() {
    const form = document.getElementById("the-form");

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

    form.brand.value = "Audi";
    form.model.value = "A5";
    form.fuel.value = "Diesel";
    form.gearbox.value = "Automata";
    form.body.value = "Sedan";
    form.color.value = "Maro";
    form.drivetrain.value = "Fata";
}
