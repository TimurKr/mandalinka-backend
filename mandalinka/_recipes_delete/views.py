# from django.shortcuts import render
# from django.contrib.auth.decorators import permission_required
# from django.http import *
# from django.urls import reverse, reverse_lazy
# from django.core.exceptions import ValidationError

# from .models import RecipeDesign
# from ingredients.models import Ingredient, IngredientVersion
# from . import forms


# # RENDER
# @permission_required('recipes.view_recipe')
# def management_view(request,
#     messages=[],
#     warnings=[],
#     new_recipe_form = None,):
#     """
#     Main page for rendering the recipe tab in management page
#     Only works with GET methods
#     """

#     if request.method != 'GET':
#         return HttpResponseBadRequest()

#     messages=[]
#     warnings=[]

#     # Generate restriction warning if it has been redirected
#     redirected_from = request.GET.get('next', None)
#     if redirected_from:
#         warnings.append('Nedostatočné privilégia')
#         if '/ingredient' in redirected_from:
#             warnings[-1] += ' na pezeranie ingrediencií'
#         else:
#             if '/add' in redirected_from:
#                 warnings[-1] += ' na pridanie nového'
#             elif '/edit' in redirected_from:
#                 warnings[-1] += ' na upravenie'
#             elif '/activate' in redirected_from:
#                 warnings[-1] += ' na aktivovanie'
#             elif '/deactivate' in redirected_from:
#                 warnings[-1] += ' na deaktivovanie'
#             elif '/retire' in redirected_from:
#                 warnings[-1] += ' na vypnutie'
#             elif '/delete' in redirected_from:
#                 warnings[-1] += ' na vymazanie'
#             warnings[-1] += ' receptu'

#     # Create message or a warning if it is in the GET data
#     m = request.GET.get('message', None)
#     if m:
#         messages.append(m)

#     # Query all recipes to render
#     recipes = {
#         RecipeDesign.Statuses.INACTIVE: RecipeDesign.objects.filter(_status=RecipeDesign.Statuses.INACTIVE)[:10],
#         RecipeDesign.Statuses.ACTIVE: RecipeDesign.objects.filter(_status=RecipeDesign.Statuses.ACTIVE)[:10],
#         RecipeDesign.Statuses.DELETED: RecipeDesign.objects.filter(_status=RecipeDesign.Statuses.DELETED)[:10],
#     }

#     # Add the editinig forms to all recipes
#     for recipe in recipes[RecipeDesign.Statuses.INACTIVE]:
#         recipe.edit_general_form = forms.EditRecipeDesignForm(recipe.id, instance=recipe, prefix=str(recipe.id))
#         recipe.edit_ingredients_formset = forms.RecipeDesignIngredientFormset(instance=recipe, prefix=str(recipe.id))
#         recipe.edit_steps_formset = forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))

#         # If steps aren't consecutive, add error to the edit_steps_formset
#         if not recipe.unique_consecutive_step_numbers() and recipe.edit_steps_formset._non_form_errors == None:
#             recipe.edit_steps_formset.full_clean()
#             recipe.edit_steps_formset._non_form_errors.append(ValidationError('Nesprávne číslovanie.'))


#     # Fill new_recipe_modal if unspecified
#     if new_recipe_form:
#         is_new_recipe_modal_active = True
#     else:
#         new_recipe_form = forms.NewRecipeDesignForm(initial={'created_by': request.user})
#         is_new_recipe_modal_active = False

#     return render(request, 'recipes/management.html', {
#         'recipes': recipes,
#         'messages': messages,
#         'warnings': warnings,
#         'name': request.user.first_name,
#         'active_tab': 'recipes',
#         'new_recipe_form': new_recipe_form,
#         'is_new_recipe_modal_active': is_new_recipe_modal_active,
#     })

# @permission_required('recipes.view_recipe')
# def info_widget(request, recipe_id):
#     # Redirect if not GET
#     if request.method != 'GET':
#         return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

#     # Redirect if recipe doesn't exist
#     try:
#         recipe = RecipeDesign.objects.get(id=recipe_id)
#     except:
#         return HttpResponseRedirect(reverse('recipes:management_page'))

#     return render(request, 'recipes/info_modal.html', {'recipe': recipe})

# @permission_required('recipes.change_recipe')
# def edit_widget(request, recipe_id):
#     # Redirect if not GET
#     if request.method != 'GET':
#         return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

#     # Redirect if recipe doesn't exist
#     try:
#         recipe = RecipeDesign.objects.get(id=recipe_id)
#         recipe.edit_general_form = forms.EditRecipeDesignForm(recipe.id, instance=recipe, prefix=str(recipe.id))
#         recipe.edit_ingredients_formset = forms.RecipeDesignIngredientFormset(instance=recipe, prefix=str(recipe.id))
#         recipe.edit_steps_formset = forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))
#     except:
#         return HttpResponseRedirect(reverse('recipes:management_page'))

#     return render(request, 'recipes/edit_modal.html', {'recipe': recipe})

# @permission_required('recipes.view_recipe')
# def load_more(request):
#     """
#     Returns rendered list of recipes
#     GET arguments:
#         'status'
#         'from'
#         'to' or 'count'
#     """
#     # If not GET request
#     if request.method != 'GET':
#         return HttpResponseBadRequest()

#     # If status not specified or invalid
#     status = request.GET.get('status', None)
#     if not status or (status, status) not in RecipeDesign.Statuses.options:
#         return HttpResponseBadRequest()

#     from_index = int(request.GET.get('from', None))

#     # If 'from' and 'to' specified
#     if from_index and request.GET.get('to', None):
#         to_index = int(request.GET.get('to'))

#     # If 'from' and 'count' specified
#     elif from_index and request.GET.get('count', None):
#         to_index = from_index + int(request.GET.get('count'))

#     else:
#         return HttpResponseBadRequest()

#     recipes = RecipeDesign.objects.filter(status=status).order_by('-last_status_change')[from_index:to_index]

#     if status is RecipeDesign.Statuses.INACTIVE:
#         for recipe in recipes:
#             recipe.edit_general_form = forms.EditRecipeDesignForm(recipe.id, instance=recipe, prefix=str(recipe.id))
#             recipe.edit_ingredients_formset = forms.RecipeDesignIngredientFormset(instance=recipe, prefix=str(recipe.id))
#             recipe.edit_steps_formset = forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))

#     return render(request, 'recipes/list_recipes.html', {'recipes':recipes})


# # ADD
# @permission_required('recipes.add_recipe', login_url='recipes:management_page')
# def add(request):
#     """
#     View for displaying a new_recipe_form and posting its data
#     """
#     if request.method == 'POST':
#         form = forms.NewRecipeDesignForm(request.POST)
#         try:
#             new_recipe = form.save(commit=False)
#             if new_recipe.created_by.id != request.user.id and not request.user.is_superuser:
#                 form.add_error('created_by', ValidationError(f'Nemáte povolenie pridávať recepty pod iným menom. Momentálne ste prihlásený ako {request.user.get_full_name()}', 'insufficient_permissions'))
#                 raise ValueError('Nemáte povolenie pridávať recepty pod iným ako vlastným menom.', 'insufficient_permissions')
#         except:
#             pass
#         else:
#             new_recipe.save()
#             return HttpResponseRedirect(reverse('recipes:management_page'))
#     else:
#         form = forms.NewRecipeDesignForm(initial={'created_by': request.user})

#     request.method = 'GET'
#     return management_view(request, new_recipe_form = form)

# @permission_required('recipes.add_recipe', login_url='recipes:management_page')
# def add_descendant(request, predecessor_id):
#     """
#     View for GETting new_recipe_form as descendant
#     For POST use add
#     """
#     if request.method != 'GET':
#         return HttpResponseBadRequest(request)

#     try:
#         predecessor = RecipeDesign.objects.get(id=predecessor_id)
#     except:
#         return HttpResponseBadRequest(request)

#     form = forms.NewRecipeDesignForm(
#         initial = {
#             'predecessor': predecessor,
#             'created_by': request.user,
#             },
#         instance = predecessor)

#     return management_view(request, new_recipe_form = form)

# # EDIT
# @permission_required('recipes.change_recipe', login_url='recipes:management_page')
# def edit_general(request, recipe_id):
#     """
#     View serving only for POSTing general recipe form data
#     """
#     # Redirect if not POST
#     if request.method != 'POST':
#         return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

#     # Redirect if recipe doesn't exist
#     try:
#         recipe = RecipeDesign.objects.get(id=recipe_id)
#     except:
#         return HttpResponseRedirect(reverse('recipes:management_page'))

#     # Process the form data
#     form = forms.EditRecipeDesignForm(recipe_id, request.POST, request.FILES, instance=recipe, prefix=str(recipe.id))
#     try:
#         form.save()
#     except:
#         # Form didn't validate
#         pass
#     else:
#         # Success
#         form = forms.EditRecipeDesignForm(recipe_id, instance=recipe, prefix=str(recipe.id))

#     return render(request, 'recipes/forms/general_form.html', {
#         'form': form,
#         'recipe': recipe,
#         })

# @permission_required('recipes.change_recipe', login_url='recipes:management_page')
# def edit_steps(request, recipe_id):
#     """
#     View serving only for POSTing recipe steps formset data
#     """
#     # Redirect if not POST
#     if request.method != 'POST':
#         return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

#     # Redirect if recipe doesn't exist
#     try:
#         recipe = RecipeDesign.objects.get(id=recipe_id)
#     except:
#         return HttpResponseRedirect(reverse('recipes:management_page'))

#     formset = forms.StepFormset(request.POST, request.FILES, queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))

#     if formset.is_valid():
#         steps = formset.save(commit=False)
#         for step in steps:
#             step.recipe = recipe
#             step.save()

#         if recipe.unique_consecutive_step_numbers():
#             # Success
#             if request.POST.get('steps_finished'):
#                 recipe.steps_finished = True
#             else:
#                 recipe.steps_finished = False
#             recipe.save()

#             formset = forms.StepFormset(queryset=recipe.steps.order_by('number'), prefix=str(recipe.id))
#         else:
#             # Steps aren't consecutive
#             formset._non_form_errors.append(ValidationError('Nesprávne číslovanie.'))
#             recipe.steps_finished = False
#             recipe.save()

#     return render(request, 'recipes/forms/steps_formset.html', {
#         'formset': formset,
#         'recipe': recipe,
#         })

# @permission_required('recipes.change_recipe', login_url='recipes:management_page')
# def edit_ingredients(request, recipe_id):
#     """
#     View serving only for POSTing recipe ingredients formset data, return new generated form
#     """
#     # Redirect if not POST
#     if request.method != 'POST':
#         return HttpResponseRedirect(reverse('recipes:render_editing_recipe', args=(recipe_id,)))

#     # Redirect if recipe doesn't exist
#     try:
#         recipe = RecipeDesign.objects.get(id=recipe_id)
#     except:
#         return HttpResponseRedirect(reverse('recipes:management_page'))

#     formset = forms.RecipeDesignIngredientFormset(request.POST, request.FILES, recipe, prefix=str(recipe.id))

#     if formset.is_valid():
#         # Success
#         formset.save()
#         if request.POST.get('ingredients_finished'):
#             recipe.ingredients_finished = True
#         else:
#             recipe.ingredients_finished = False
#         recipe.save()
#         formset = forms.RecipeDesignIngredientFormset(instance=recipe, prefix=str(recipe.id))


#     return render(request, 'recipes/forms/ingredients_formset.html', {
#         'formset': formset,
#         'recipe': recipe,
#         })


# # ACTIVATE
# @permission_required('recipes.change_recipe_status', login_url='recipes:management_page')
# def activate(request, recipe_id):
#     RecipeDesign.objects.get(id=recipe_id).activate()
#     return HttpResponseRedirect(reverse('recipes:management_page'))

# # DEACTIVATE
# @permission_required('recipes.change_recipe_status', login_url='recipes:management_page')
# def deactivate(request, recipe_id):
#     RecipeDesign.objects.get(id=recipe_id).deactivate()
#     return HttpResponseRedirect(reverse('recipes:management_page'))

# # RETIRE
# @permission_required('recipes.change_recipe_status', login_url='recipes:management_page')
# def retire(request, recipe_id):
#     RecipeDesign.objects.get(id=recipe_id).retire()
#     return HttpResponseRedirect(reverse('recipes:management_page'))


# # INGEDIENTS ######################################################################################

# # LIST
# # @permission_required('recipes.view_ingredient', login_url='recipes:manage')
# # def list_ingredients(request):

# #     redirected_from = request.GET.get('next', None)
# #     warning = None
# #     if redirected_from:
# #         warning = 'Nedostatočné privilégia'
# #         if '/add' in redirected_from:
# #             warning += ' na pridanie novej'
# #         elif '/edit' in redirected_from:
# #             warning += ' na upravenie'
# #         elif '/activate' in redirected_from:
# #             warning += ' na aktivovanie'
# #         elif '/deactivate' in redirected_from:
# #             warning += ' na deaktivovanie'
# #         elif '/delete' in redirected_from:
# #             warning += ' na vymazanie'
# #         warning += ' ingrediencie'

# #     ingredients = {
# #         'active': Ingredient.objects.filter(is_active=True),
# #         'inactive': Ingredient.objects.filter(is_active=False),
# #     }
# #     return render(request, 'recipes/ingredients/list.html', {
# #             'warning': warning,
# #             'ingredients': ingredients,
# #         })


# # # ADD
# # @permission_required('recipes.add_ingredient', login_url='recipes:list_ingredients')
# # def add_ingredient(request):
# #     if request.method == 'POST':
# #         form = forms.NewIngredientForm(request.POST)
# #         try:
# #             ingredient = form.save(commit=False)
# #         except ValueError as e:
# #             pass
# #         else:
# #             if 'aktivovať' in request.POST['submit']:
# #                 ingredient.activate()
# #             ingredient.save()
# #             form.save_m2m()
# #             return HttpResponseRedirect(reverse('recipes:list_ingredients'))
# #     else:
# #         form = forms.NewIngredientForm(initial={'created_by': request.user.id})
# #     return render(request, 'recipes/ingredients/add.html', {'form': form})


# # # EDIT
# # @permission_required('recipes.change_ingredient', login_url='recipes:list_ingredients')
# # def edit_ingredient(request, ingredient_id):
# #     try:
# #         ingredient = Ingredient.objects.get(id=ingredient_id)
# #     except:
# #         return HttpResponseRedirect(reverse('recipes:list_ingredients'))

# #     if request.method == 'POST':
# #         form = forms.EditIngredientForm(ingredient_id, request.POST, instance=ingredient)
# #         try:
# #             ingredient = form.save(commit=False)
# #         except ValueError:
# #             pass
# #         else:
# #             if 'aktivovať' in request.POST['submit']:
# #                 ingredient.activate()
# #             ingredient.save()
# #             form.save_m2m()
# #             return HttpResponseRedirect(reverse('recipes:list_ingredients'))
# #     else:
# #         form = forms.EditIngredientForm(ingredient_id, instance=ingredient)
# #     return render(request,"recipes/ingredients/edit.html", {'form':form})


# # # ACTIVATE
# # @permission_required('recipes.toggle_is_active_ingredient', login_url='recipes:list_ingredients')
# # def activate_ingredient(request, ingredient_id):
# #     Ingredient.objects.get(id=ingredient_id).activate()
# #     return HttpResponseRedirect(reverse('recipes:list_ingredients'))


# # # DEACTIVATE
# # @permission_required('recipes.toggle_is_active_ingredient', login_url='recipes:list_ingredients')
# # def deactivate_ingredient(request, ingredient_id):
# #     Ingredient.objects.get(id=ingredient_id).deactivate()
# #     return HttpResponseRedirect(reverse('recipes:list_ingredients'))
