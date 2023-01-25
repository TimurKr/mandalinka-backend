document.addEventListener("DOMContentLoaded", () => {
    let ingredient_forms = document.querySelectorAll(".form-in-ingredients_formset")
    let empty_form = ingredient_forms[ingredient_forms.length - 1].cloneNode(true)

    let formset = document.querySelector("#ingredients-form")
    let add_button = document.querySelector("#add-ingredient")
    let total_forms_field = document.querySelector("#id_ingredients_mid-TOTAL_FORMS")
    let max_forms = document.querySelector("#id_ingredients_mid-MAX_NUM_FORMS").value


    function check_form_limit() {
        if (total_forms_field.value == max_forms) {
            add_button.disabled = true
            add_button.innerHTML = `Maximum ingrediencií (${max_forms}) dosiahnuté`
        }
        else {
            add_button.disabled = false
        }
    }

    add_button.addEventListener("click", (e) => {
        e.preventDefault()

        let new_form_number = total_forms_field.value
             
        empty_form.innerHTML = empty_form.innerHTML.replace(RegExp(`ingredients_mid-(\\d){1}-`,'g'), `ingredients_mid-${new_form_number}-`)

        ingredient_forms = document.querySelectorAll(".form-in-ingredients_formset")
        ingredient_forms[ingredient_forms.length - 1].after(empty_form.cloneNode(true))
        ingredient_forms = document.querySelectorAll(".form-in-ingredients_formset")
        
        document.getElementById(`id_ingredients_mid-${total_forms_field.value}-ingredient`).focus()

        total_forms_field.value++

        check_form_limit()
    })

    check_form_limit()
})