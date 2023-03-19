"use client";

import { Formik, Form, Field, FieldArray } from "formik";
import * as Yup from "yup";
import TextInput from "@/components/form_elements/text";
import MultiSelectInput from "@/components/form_elements/select_multiple";
import FileInput from "@/components/form_elements/file";
import SelectInput from "@/components/form_elements/select";
import Button from "@/components/button";
import { useRouter } from "next/navigation";
import { useState } from "react";
import ErrorMessage from "@/components/form_elements/error_message";
import Alert from "@/components/alert";
import parseInvalidResponse from "@/components/form_elements/parse_invalid_response";
import { Unit } from "@/components/fetching/units";
import { Attribute } from "@/components/fetching/attributes";
import { Diet } from "@/components/fetching/diets";
import { KitchenAccessory } from "@/components/fetching/kitchen_accesories";
import CheckBoxInput from "@/components/form_elements/checkbox";
import NumberInput from "@/components/form_elements/number";
import TextAreaInput from "@/components/form_elements/text_area";
import { BorderedElement } from "@/components/bordered_element";

interface StepValues {
  number: number;
  text: string;
  thumbnail: File | null;
}

interface IngredientValues {
  ingredient: number | null;
  alternative_for: IngredientValues | null;
  amount: number;
  unit: number;
  text: string;
}

interface RecipeValues {
  name: string;
  description: string;
  thumbnail: File | null;
  predecessor: number | "";
  exclusive_inheritance: boolean;
  steps: StepValues[];
  ingredients: IngredientValues[];
  difficulty: number;
  cooking_time: number;
  active_cooking_time: number;
  attributes: number[];
  diets: number[];
  required_accessories: number[];
  description_finished: boolean;
  steps_finished: boolean;
  ingredients_finished: boolean;
  todo: string;
  price: number;
}

export default function RecipeDesignForm({
  title,
  submit_url,
  method,
  options,
  initial,
}: {
  title?: string;
  submit_url: string;
  method: "POST" | "PATCH";
  options: {
    units: { value: string; label: string }[];
    attributes: { value: string; label: string }[];
    diets: { value: string; label: string }[];
    kitchen_accesories: { value: string; label: string }[];
    recipes: { value: string; label: string }[];
    ingredients: { value: string; label: string }[];
  };
  initial?: RecipeValues;
}) {
  console.log(options);
  const [errorMessage, setErrorMessage] = useState<string | null>("Testujem");

  let initialValues: RecipeValues = initial || {
    name: "",
    description: "",
    thumbnail: null,
    predecessor: "",
    exclusive_inheritance: true,
    steps: [],
    ingredients: [],
    difficulty: 2,
    cooking_time: 0,
    active_cooking_time: 0,
    attributes: [],
    diets: [],
    required_accessories: [],
    description_finished: false,
    steps_finished: false,
    ingredients_finished: false,
    todo: "",
    price: 0,
  };

  const validationSchema = Yup.object({
    name: Yup.string().required("Názov je povinný"),
    description: Yup.string().required("Popis je povinný"),
    // thumbnail: Yup.mixed()
    //   .test(
    //     "fileSize",
    //     "Image must be less than 1MB",
    //     (value) => value && value.size <= 1000000
    //   )
    //   .test(
    //     "fileType",
    //     "Only JPG, JPEG, PNG, or GIF images are allowed",
    //     (value) =>
    //       value &&
    //       ["image/jpg", "image/jpeg", "image/png", "image/gif"].includes(
    //         value.type
    //       )
    //   ),
    steps: Yup.array().of(
      Yup.object({
        text: Yup.string().required("Popis kroku je povinný"),
        // thumbnail: Yup.mixed()
      })
    ),
    ingredients: Yup.array().of(
      Yup.object({
        amount: Yup.number().required("Amount is required").moreThan(0, ""),
        text: Yup.string().required("Text is required"),
      })
    ),
    difficulty: Yup.number()
      .required("Zvolte nátočnosť")
      .min(1, "Minimálna náročnosť je 1")
      .max(5, "Maximálna náročnosť je 5"),
    cooking_time: Yup.number()
      .required("Zadajte čas varenia")
      .min(0, "Minimálny čas varenia je 0")
      .max(1000, "Maximálny čas prípravy je 1000"),
    active_cooking_time: Yup.number()
      .required("Zadajte čas aktívneho varenia")
      .min(0, "Minimálny čas aktívneho varenia je 0")
      .max(1000, "Maximálny čas aktívneho varenia je 1000")
      .lessThan(
        Yup.ref("cooking_time"),
        "Čas aktívneho varenia musí byť menší ako celkový čas varenia"
      ),
    attributes: Yup.array().of(Yup.number()),
    diets: Yup.array().of(Yup.number()),
    required_accessories: Yup.array().of(Yup.number()),
    description_finished: Yup.boolean(),
    steps_finished: Yup.boolean(),
    ingredients_finished: Yup.boolean(),
  });

  async function handleSubmit(
    values: RecipeValues,
    {
      setSubmitting,
      setFieldError,
    }: {
      setSubmitting: (isSubmitting: boolean) => void;
      setFieldError: (field: string, errorMsg: string) => void;
    }
  ) {
    const formData = new FormData();
    formData.append("name", values.name);
    formData.append("description", values.description);
    if (values.thumbnail) formData.append("thumbnail", values.thumbnail);

    formData.append("predecessor", values.predecessor?.toString() || "false");
    formData.append(
      "exclusive_inheritance",
      values.exclusive_inheritance.toString()
    );
    formData.append("difficulty", values.difficulty.toString());
    formData.append("cooking_time", values.cooking_time.toString());
    formData.append(
      "active_cooking_time",
      values.active_cooking_time.toString()
    );
    formData.append(
      "description_finished",
      values.description_finished.toString()
    );
    formData.append("steps_finished", values.steps_finished.toString());
    formData.append(
      "ingredients_finished",
      values.ingredients_finished.toString()
    );
    formData.append("todo", values.todo);
    formData.append("price", values.price.toString());

    values.steps.forEach((step: StepValues, index) => {
      formData.append(`steps[${index}][text]`, step.text);
      if (step.thumbnail) {
        formData.append(`steps[${index}][thumbnail]`, step.thumbnail);
      }
    });

    values.ingredients.forEach((ingredient: IngredientValues, index) => {
      if (!ingredient.ingredient) return;

      formData.append(
        `ingredients[${index}][ingredient]`,
        ingredient.ingredient.toString()
      );
      if (ingredient.alternative_for)
        formData.append(
          `ingredients[${index}][alternative_for]`,
          ingredient.alternative_for.toString()
        );
      formData.append(
        `ingredients[${index}][amount]`,
        ingredient.amount.toString()
      );
      formData.append(
        `ingredients[${index}][unit]`,
        ingredient.unit.toString()
      );
      formData.append(`ingredients[${index}][text]`, ingredient.text);
    });

    values.attributes.forEach((attribute: number, index) => {
      formData.append(`attributes`, attribute.toString());
    });

    values.diets.forEach((diet: number, index) => {
      formData.append(`diets`, diet.toString());
    });

    values.required_accessories.forEach((accessory: number, index) => {
      formData.append(`required_accessories`, accessory.toString());
    });

    Object.entries(values).forEach(([key, value]) => {
      console.log(key, value);
    });

    // await fetch(submit_url, {
    //   method: method,
    //   body: formData,
    // })
    //   .then((response) =>
    //     parseInvalidResponse(response, setFieldError, setErrorMessage)
    //   )
    //   .then(async (response) => {
    //     if (response.ok) {
    //       let json = await response.json();
    //       window.location.href = `/management/ingredients/${json.id}/`;
    //     }
    //   });

    setSubmitting(false);
  }

  return (
    <>
      {title && (
        <div className="w-full">
          <h1 className="text-primary p-3 text-center text-2xl font-bold">
            {title}
          </h1>
        </div>
      )}
      <Alert variant="danger" onClose={() => setErrorMessage(null)}>
        {errorMessage}
      </Alert>
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {(props) => (
          <Form className="flex flex-wrap gap-2 p-2">
            <div className="grid grow grid-cols-3 gap-2">
              <div className="col-span-2 row-span-2">
                <FileInput name="thumbnail" label="Náhľadový obrázok" />
              </div>
              <div>
                <TextInput name="name" label="Názov" />
              </div>
              <div>
                <TextAreaInput name="description" label="Popis" />
              </div>
              <div>
                <BorderedElement>
                  <div>
                    <SelectInput
                      name="predecessor"
                      label="Predchádzajúca receptúra"
                      options={[
                        ...options.recipes,
                        { value: "", label: "Bez dedenia" },
                      ]}
                    />
                  </div>
                  <div>
                    <CheckBoxInput
                      name="exclusive_inheritance"
                      label="Výhradné dedenie"
                    />
                  </div>
                  <div>
                    <Button
                      variant="primary"
                      onClick={() =>
                        console.log("Pokus o aplikáciu predacessor")
                      }
                    >
                      Vyplniť predchodcom
                    </Button>
                  </div>
                </BorderedElement>
              </div>
            </div>

            <div>
              <BorderedElement title="Postup">Steps</BorderedElement>
            </div>
            <div>
              <BorderedElement title="Ingrediencie" className="shrink">
                Ingrediencie
              </BorderedElement>
            </div>
            <div>
              <SelectInput
                name="predecessor"
                label="Predchádzajúca receptúra"
                options={[
                  ...options.recipes,
                  { value: "", label: "Bez dedenia" },
                ]}
              />
            </div>
            <div>
              <CheckBoxInput
                name="exclusive_inheritance"
                label="Výhradné dedenie"
              />
            </div>
            <div>
              <SelectInput
                name="difficulty"
                label="Obtiažnosť"
                options={[
                  { value: 1, label: "Ľahká" },
                  { value: 2, label: "Stredne ťažká" },
                  { value: 3, label: "Ťažká" },
                  { value: 4, label: "Pre profesionálov" },
                ]}
              />
            </div>
            <div>
              <NumberInput name="cooking_time" label="Celkový čas prípravy" />
            </div>
            <div>
              <NumberInput
                name="active_cooking_time"
                label="Aktívny čas prípravy"
              />
            </div>
            <div>
              <NumberInput name="price" label="Cena" />
            </div>
            <div>
              <TextInput name="todo" label="Čo ešte treba spraviť" />
            </div>
            <div>
              <CheckBoxInput
                name="description_finished"
                label="Popis dokončený"
              />
            </div>
            <div>
              <CheckBoxInput name="steps_finished" label="Kroky dokončené" />
            </div>
            <div>
              <CheckBoxInput
                name="ingredients_finished"
                label="Zoznam ingrediencií dokončený"
              />
            </div>
            <div>
              <MultiSelectInput
                name="diets"
                label="Diéty"
                options={options.diets}
              />
            </div>
            <div>
              <MultiSelectInput
                name="attributes"
                label="Atribúty"
                options={options.attributes}
              />
            </div>
            <div>
              <MultiSelectInput
                name="required_accessories"
                label="Potrebné príslušenstvo"
                options={options.kitchen_accesories}
              />
            </div>
            <div>
              <FieldArray name="steps">
                {({ push, remove }) => (
                  <>
                    {props.values.steps.map((step: any, index: number) => (
                      <div key={index}>
                        <TextInput
                          name={`steps.${index}.text`}
                          label={`Krok ${index + 1}`}
                        />
                        <FileInput
                          name={`steps.${index}.thumbnail`}
                          label={`Náhľadový obrázok kroku ${index + 1}`}
                        />
                        <Button variant="danger" onClick={() => remove(index)}>
                          Odstrániť krok
                        </Button>
                      </div>
                    ))}
                    <Button
                      variant="success"
                      onClick={() => push({ text: "", thumbnail: null })}
                    >
                      Pridať krok
                    </Button>
                  </>
                )}
              </FieldArray>
            </div>
            <div>
              <FieldArray name="ingredients">
                {({ push, remove }) => (
                  <>
                    {props.values.ingredients.map(
                      (ingredient: any, index: number) => (
                        <div key={index}>
                          <SelectInput
                            name={`ingredients.${index}.ingredient`}
                            label={`Ingrediencia ${index + 1}`}
                            options={options.ingredients}
                          />
                          <NumberInput
                            name={`ingredients.${index}.amount`}
                            label={`Množstvo ingrediencie ${index + 1}`}
                          />
                          <SelectInput
                            name={`ingredients.${index}.unit`}
                            label={`Jednotka ingrediencie ${index + 1}`}
                            options={options.units}
                          />
                          <Button
                            variant="danger"
                            onClick={() => remove(index)}
                          >
                            Odstrániť ingredienciu
                          </Button>
                        </div>
                      )
                    )}
                    <Button
                      variant="success"
                      onClick={() =>
                        push({ ingredient: "", amount: 0, unit: "" })
                      }
                    >
                      Pridať ingredienciu
                    </Button>
                  </>
                )}
              </FieldArray>
            </div>
            <div className="w-full">
              <Button
                variant="primary"
                type="submit"
                disabled={props.isSubmitting}
              >
                {props.isSubmitting ? "Ukladám..." : "Uložiť"}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </>
  );
}
