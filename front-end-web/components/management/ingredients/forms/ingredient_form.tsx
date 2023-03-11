"use client";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import TextInput from "@/components/form_elements/text";
import MultiSelect from "@/components/form_elements/select_multiple";
import FileInput from "@/components/form_elements/file";
import Select from "@/components/form_elements/select";
import Button from "@/components/button";
import { Alergen } from "@/components/fetching/alergens";
import { Unit } from "@/components/fetching/units";
import { useRouter } from "next/navigation";
import { useState } from "react";
import ErrorMessage from "@/components/form_elements/error_message";
import DangerAlert from "@/components/alerts/danger";

interface IngredientValues {
  name: string;
  extra_info: string;
  img: File | null | string;
  alergens: number[];
  unit: number | "";
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
  method: "POST" | "PATCH";
  options: { alergens: Alergen[]; units: Unit[] };
  initial?: IngredientValues;
}) {
  const Router = useRouter();

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

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
    const formData = new FormData();
    formData.append("name", values.name);
    formData.append("extra_info", values.extra_info);
    formData.append("unit", values.unit.toString());
    values.alergens.forEach((alergen) => {
      formData.append("alergens", alergen.toString());
    });

    if (values.img) {
      formData.append("img", values.img);
    }

    const response = await fetch(submit_url, {
      method: method,
      body: formData,
    });

    if (!response.ok) {
      let response_json = await response.json();
      console.log("Response: ", response_json);
      setErrorMessage(response_json.detail);
      throw new Error(`HTTP error! status: ${response.status}`);
    } else {
      let response_json = await response.json();
      // TODO: Force refresh fetches
      Router.push(`/management/ingredients/${response_json.id}`);
    }

    setSubmitting(false);
  }

  const initialValues: IngredientValues = {
    name: initial ? initial.name : "",
    extra_info: initial ? initial.extra_info : "",
    img: null,
    alergens: initial ? initial.alergens : [],
    unit: initial ? initial.unit : "",
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={Yup.object({
        name: Yup.string().required("Zadajte názov"),
        unit: Yup.string().required("Vyberte jednotku"),
        extra_info: Yup.string(),
      })}
      onSubmit={handleSubmit}
    >
      <Form className="m-2 grid grid-cols-2 items-center gap-2">
        {title && (
          <div className="col-span-2">
            <h1 className="text-primary text-center text-2xl font-bold">
              {title}
            </h1>
          </div>
        )}
        {errorMessage && (
          <DangerAlert onClose={() => setErrorMessage(null)}>
            {errorMessage}
          </DangerAlert>
        )}
        <div className="row-span-3">
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
          <TextInput label="Extra informácie" name="extra_info" />
        </div>
        <div>
          <Select label="Jednotka" name="unit" options={units} />
        </div>

        <div className="col-span-2 rounded-lg border border-gray-300 p-2 md:col-span-1">
          <MultiSelect label="Alergeny" name="alergens" options={alergens} />
        </div>
        <div className="col-span-2 grid place-content-center md:col-span-1">
          <Button color="primary" dark type="submit">
            {method === "POST" ? "Pridať" : method === "PATCH" ? "Uložiť" : ""}
          </Button>
        </div>
      </Form>
    </Formik>
  );
}
