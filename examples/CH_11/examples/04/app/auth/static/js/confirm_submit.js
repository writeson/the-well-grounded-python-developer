function confirm_submit_initialize(form_name, button_name) {
    const update_button = document.getElementById(button_name);
    update_button.addEventListener('click', () => {
        document[form_name].submit();
    });
}