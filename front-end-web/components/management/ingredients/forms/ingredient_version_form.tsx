"use client";

import { Formik, Form } from "formik";
import * as Yup from "yup";
import TextInput from "@/components/form_elements/text";
import NumberInput from "@/components/form_elements/number";
import Select from "@/components/form_elements/select";
import Button from "@/components/button";
import { useRouter } from "next/navigation";

import { Unit } from "@/components/fetching/units";
import { IngredientDetail } from "../../../fetching/ingredient_detail";
import { useState } from "react";
import DangerAlert from "@/components/alerts/danger";

interface IngredientVersionValues {
  cost: number;
  amount: number;
  unit: number;
  source: string;
}

export default function IngredientVersionForm({
  title,
  submit_url,
  method,
  initial,
  unit_options,
  ingredient,
}: {
  title?: string;
  submit_url: string;
  method: "POST" | "PATCH";
  initial?: IngredientVersionValues;
  unit_options: Unit[];
  ingredient: IngredientDetail;
}) {
  const Router = useRouter();

  const [formError, setFormError] = useState<string | null>(null);

  async function handleSubmit(
    values: IngredientVersionValues,
    {
      setSubmitting,
      setFieldError,
    }: {
      setSubmitting: (isSubmitting: boolean) => void;
      setFieldError: (field: string, errorMsg: string) => void;
    }
  ) {
    const formData = new FormData();
    formData.append("ingredient", ingredient.id.toString());
    formData.append("cost", values.cost.toString());
    formData.append("amount", values.amount.toString());
    formData.append("unit", values.unit.toString());
    formData.append("source", values.source);

    // formData.forEach((value, key) => {
    //   console.log(key, value);
    // });

    const response = await fetch(submit_url, {
      method: method,
      body: formData,
    });

    let response_json = await response.json();
    if (!response.ok) {
      Object.keys(response_json).forEach((key: string) => {
        if (key === "non_field_errors") {
          setFormError(response_json[key]);
        } else {
          setFieldError(key, response_json[key]);
        }
      });
      console.log("Response: ", response_json);
    } else {
      console.log("Response ok: ", response_json);
      // TODO: Force refresh fetches
      Router.push(
        `/management/ingredients/${response_json.ingredient}/${response_json.id}`
      );
    }
  }

  const initialValues = {
    cost: initial?.cost || 0,
    amount: 1,
    unit: ingredient.unit,
    source: initial?.source || "",
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={Yup.object({
        cost: Yup.number()
          .required("Povinné pole")
          .moreThan(0, "Zadajte kladné číslo"),
        source: Yup.string().required("Povinné pole"),
      })}
      onSubmit={handleSubmit}
    >
      <Form className="grid grid-cols-1 items-center gap-y-2 ">
        {title && (
          <div className="col-span-2 pb-3">
            <h1 className="text-primary text-center text-2xl font-bold">
              {title}
            </h1>
          </div>
        )}
        {formError && (
          <div className="py-2">
            <DangerAlert>{formError}</DangerAlert>
          </div>
        )}
        <div className="col-span-2 flex items-center justify-between gap-2">
          <div className="flex-auto">
            <NumberInput label="Cena" name="cost" />
          </div>
          <p className="shrink-0 self-center">€ na</p>
          <div className="flex-auto">
            <NumberInput label="Množstvo" name="amount" />
          </div>
          <div className="flex-none">
            <Select
              label="Jednotka"
              name="unit"
              options={unit_options.map((unit) => ({
                value: unit.id,
                label: unit.name,
              }))}
            />
          </div>
        </div>

        <div className="col-span-2">
          <TextInput label="Zdroj" name="source" />
        </div>

        <div className="col-span-2 grid place-content-center md:col-span-1">
          <Button style="primary" dark type="submit">
            {method === "POST" ? "Pridať" : method === "PATCH" ? "Uložiť" : ""}
          </Button>
        </div>
      </Form>
    </Formik>
  );
}
