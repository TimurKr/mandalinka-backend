"use client";

import { Formik, Form } from "formik";
import * as Yup from "yup";
import TextInput from "@/components/form_elements/text";
import NumberInput from "@/components/form_elements/number";
import SelectInput from "@/components/form_elements/select";
import Button from "@/components/button";
import { useRouter } from "next/navigation";

import { Unit } from "@/components/fetching/units";
import { IngredientDetail } from "../../../fetching/ingredient_detail";
import { useState } from "react";
import Alert from "@/components/alert";
import parseInvalidResponse from "@/components/form_elements/parse_invalid_response";

interface IngredientVersionValues {
  source: string;
  expiration_period: number;
}

export default function IngredientVersionForm({
  title,
  submit_url,
  method,
  initial,
  ingredient,
}: {
  title?: string;
  submit_url: string;
  method: "POST" | "PATCH";
  initial?: IngredientVersionValues;
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
    formData.append("source", values.source);
    formData.append("expiration_period", values.expiration_period.toString());
    await fetch(submit_url, {
      method: method,
      body: formData,
    })
      .then((response) =>
        parseInvalidResponse(response, setFieldError, setFormError)
      )
      .then(async (response) => {
        if (response.ok) {
          let json = await response.json();
          window.location.href = `/management/ingredients/${json.ingredient}/${json.id}`;
        }
      });
  }

  const initialValues = {
    source: initial?.source || "",
    expiration_period: initial?.expiration_period || 7,
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={Yup.object({
        source: Yup.string().required("Povinné pole"),
        expiration_period: Yup.number()
          .min(1, "Musí byť viac ako 1")
          .integer("Zadajte celé číslo")
          .required("Povinné pole"),
      })}
      onSubmit={handleSubmit}
    >
      {(props) => (
        <Form className="flex flex-wrap items-center justify-between gap-2">
          {title && (
            <div className="w-full pb-2">
              <h1 className="text-primary text-center text-2xl font-bold">
                {title}
              </h1>
            </div>
          )}
          <Alert
            className="w-full"
            variant="danger"
            onClose={() => setFormError(null)}
          >
            {formError}
          </Alert>
          <div className="grow">
            <TextInput label="Zdroj" name="source" />
          </div>
          <div className="">
            <NumberInput
              label="Priemerná doba trvanlivosti"
              name="expiration_period"
            />
          </div>
          <div className="grid place-content-center">
            <Button
              variant="primary"
              dark
              type="submit"
              disabled={props.isSubmitting}
            >
              {method === "POST"
                ? "Vytvoriť"
                : method === "PATCH"
                ? "Uložiť"
                : ""}
            </Button>
          </div>
        </Form>
      )}
    </Formik>
  );
}
