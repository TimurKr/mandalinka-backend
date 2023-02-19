"use client";

import { Formik, Form, Field } from "formik";
import { TextInput } from "@/components/form_elements/text";
import { MultiSelect } from "@/components/form_elements/select_multiple";
import { FileInput } from "@/components/form_elements/files";
import { Select } from "@/components/form_elements/select";

const alergens = [
  { value: "1", label: "Gluten" },
  { value: "2", label: "Mlieko" },
  { value: "3", label: "Vajca" },
  { value: "4", label: "Ryby" },
];

const units = [
  { value: "1", label: "Kg" },
  { value: "2", label: "g" },
  { value: "3", label: "L" },
  { value: "4", label: "ml" },
  { value: "5", label: "ks" },
];

interface NewIngredientValues {
  name: string;
  img: string;
  alergens: number[];
  unit: string;
}

export default function NewIngredientForm() {
  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>): void {
    event.preventDefault();
    console.log("Submitted");
  }

  return (
    <Formik
      initialValues={{ name: "", alergens: [], img: "", unit: "" }}
      onSubmit={(values, { setSubmitting }) => {
        setTimeout(() => {
          alert(JSON.stringify(values, null, 2));
          setSubmitting(false);
        }, 400);
      }}
    >
      <Form className="grid grid-cols-2 items-center gap-2">
        <div className="col-span-2">
          <h1 className="text-primary text-center text-2xl font-bold">
            Nová ingriediencia
          </h1>
        </div>
        <div className="col-span-2 row-span-3 md:col-span-1">
          <FileInput label="Obrázok" name="img" />
        </div>
        <div>
          <TextInput label="Názov" name="name" />
        </div>
        <div>
          <Select label="Jednotka" name="unit" options={units} />
        </div>

        <div className="col-span-2 rounded-lg border border-gray-300 p-2 shadow md:col-span-1">
          <MultiSelect label="Alergeny" name="alergens" options={alergens} />
        </div>
        <div>
          <button
            type="submit"
            className="bg-primary-400 block w-full rounded-full px-3  py-2 text-center text-black shadow-md hover:shadow-xl focus:shadow-xl sm:text-sm"
          >
            Submit
          </button>
        </div>
      </Form>
    </Formik>
  );
}
