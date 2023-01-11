function create_add_button(formset_prefix) {
    var formset = document.getElementById(`ingredients-formset-${formset_prefix}`)

    let ingredient_forms = formset.querySelectorAll(`.form-in-ingredients_formset`)

    let empty_form = ingredient_forms[ingredient_forms.length - 1].cloneNode(true)

    let add_button = formset.querySelector(`#add-ingredient-${formset_prefix}`)
    let total_forms_field = formset.querySelector(`#id_${formset_prefix}-TOTAL_FORMS`)
    let max_forms = formset.querySelector(`#id_${formset_prefix}-MAX_NUM_FORMS`).value


    function check_form_limit() {
        if (total_forms_field.value == max_forms) {
            add_button.disabled = true
            add_button.innerHTML = `Maximum ingrediencií (${max_forms}) dosiahnuté`
        }
        else {
            add_button.disabled = false
        }
    }

    add_button.onclick = (e) => {
        e.preventDefault()

        let new_form_number = total_forms_field.value
             
        empty_form.innerHTML = empty_form.innerHTML.replace(RegExp(`${formset_prefix}-${new_form_number-1}`,'g'), `${formset_prefix}-${new_form_number}`)

        ingredient_forms = formset.querySelectorAll(`.form-in-ingredients_formset`)
        ingredient_forms[ingredient_forms.length - 1].after(empty_form.cloneNode(true))
        ingredient_forms = formset.querySelectorAll(`.form-in-ingredients_formset`)
          
        total_forms_field.value++
        
        check_form_limit()
        
        let new_focus_field = document.getElementById(`id_${formset_prefix}-${total_forms_field.value-1}-ingredient`)
        new_focus_field.focus()
    }

    check_form_limit()
}


function execute_all_ingredient_forms() {
    document.querySelectorAll(".ingredients-formset").forEach(element => {
        create_add_button(element.getAttribute('prefix'))
    });
}

document.addEventListener('DOMContentLoaded', execute_all_ingredient_forms)