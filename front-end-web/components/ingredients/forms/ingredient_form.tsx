"use client";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { TextInput } from "@/components/form_elements/text";
import { MultiSelect } from "@/components/form_elements/select_multiple";
import { FileInput } from "@/components/form_elements/file";
import { Select } from "@/components/form_elements/select";
import Button from "@/components/button";
import { Options } from "./fetch_options";
import { useRouter } from "next/navigation";

interface IngredientValues {
  name: string;
  img: File | null | string;
  alergens: number[];
  unit: string;
}

export default function IngredientForm({
  title,
  submit_url,
  method,
  options,
  initial,
}: {
  title?: string;
  submit_url: string;
  method: "POST" | "PUT";
  options: Options;
  initial?: IngredientValues;
}) {
  const Router = useRouter();

  const alergens = options.alergens.map((alergen) => ({
    value: alergen.code,
    label: alergen.name,
  }));

  const units = options.units.map((unit) => ({
    value: unit.id,
    label: unit.name,
  }));

  async function handleSubmit(
    values: IngredientValues,
    { setSubmitting }: { setSubmitting: (isSubmitting: boolean) => void }
  ) {
    console.log(values);
    // const formData = new FormData();
    // formData.append("name", values.name);
    // formData.append("unit", values.unit.toString());
    // values.alergens.forEach((alergen) => {
    //   formData.append("alergens", alergen.toString());
    // });

    // if (values.img) {
    //   formData.append("img", values.img);
    // }

    // console.log(formData.get("img"));

    // const response = await fetch(submit_url, {
    //   method: method,
    //   body: formData,
    // });

    // if (!response.ok) {
    //   console.log("Response: ", response);
    //   throw new Error(`HTTP error! status: ${response.status}`);
    // } else {
    //   let response_json = await response.json();
    //   // TODO: Force refresh the search bar, now when new ingredient is created, it doesn't refresh
    //   Router.push(`/management/ingredients/${response_json.id}`);
    // }

    // setSubmitting(false);
  }

  const initialValues: IngredientValues = {
    name: initial ? initial.name : "",
    img: null,
    alergens: initial ? initial.alergens : [],
    unit: initial ? initial.unit : "",
  };

  console.log(initialValues);

  return (
    <Formik
      // If initial is defined, pass initial to initialValues, but without img
      // because img is a File object, and we don't want to pass it to initialValues

      initialValues={initialValues}
      validationSchema={Yup.object({
        name: Yup.string().required("Zadajte názov"),
        unit: Yup.string().required("Vyberte jednotku"),
      })}
      onSubmit={handleSubmit}
    >
      <Form className="grid grid-cols-2 items-center gap-2">
        {title && (
          <div className="col-span-2">
            <h1 className="text-primary text-center text-2xl font-bold">
              {title}
            </h1>
          </div>
        )}
        <div className="col-span-2">
          <FileInput
            label="Obrázok"
            name="img"
            initial_url={
              initial && initial.img && typeof initial.img === "string"
                ? initial.img
                : undefined
            }
          />
        </div>
        <div>
          <TextInput label="Názov" name="name" />
        </div>
        <div>
          <Select label="Jednotka" name="unit" options={units} />
        </div>

        <div className="col-span-2 rounded-lg border border-gray-300 p-2 md:col-span-1">
          <MultiSelect label="Alergeny" name="alergens" options={alergens} />
        </div>
        <div className="col-span-2 grid place-content-center md:col-span-1">
          <Button style="primary" dark type="submit">
            Pridať
          </Button>
        </div>
      </Form>
    </Formik>
  );
}
