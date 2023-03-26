"use client";

// import { Formik, Form, Field } from "formik";
// import * as Yup from "yup";
// import TextInput from "@/components/form_elements/text";
// import MultiSelectInput from "@/components/form_elements/select_multiple";
// import FileInput from "@/components/form_elements/file";
// import SelectInput from "@/components/form_elements/select";
// import Button from "@/components/button";
// import { Alergen } from "@/components/fetching/alergens";
// import { Unit } from "@/components/fetching/units";
// import { useRouter } from "next/navigation";
// import { useState } from "react";
// import ErrorMessage from "@/components/form_elements/error_message";
// import Alert from "@/components/alert";
// import {
//   gql,
//   useMutation,
//   useSuspenseQuery_experimental as useSuspenseQuery,
// } from "@apollo/client";
// import { GraphQLError } from "graphql";

// type IngredientValues = {
//   name: string;
//   extra_info: string;
//   img: File | null | string;
//   alergens: number[];
//   unit: number | "";
// };

// const validationSchema = Yup.object({
//   name: Yup.string().required("Zadajte názov ingrediencie"),
//   extra_info: Yup.string(),
//   img: Yup.mixed().test("fileSize", "Súbor je príliš veľký", (value) => {
//     if (value instanceof File) {
//       return value.size <= 1000000;
//     }
//     return true;
//   }),
//   alergens: Yup.array().of(Yup.number()),
//   unit: Yup.number().required("Zadajte jednotku"),
// });

// const ADD_INGREDIENT = gql`
//   mutation CreateIngredient(
//     $name: String!
//     $extra_info: String
//     $img: String
//     $alergens: [Int!]
//     $unit: Int!
//   ) {
//     createIngredient(
//       name: $name
//       extra_info: $extra_info
//       img: $img
//       alergens: $alergens
//       unit: $unit
//     ) {
//       id
//       name
//       extra_info
//       img
//       alergens {
//         id
//         name
//       }
//       unit {
//         id
//         name
//         sign
//       }
//     }
//   }
// `;

// export default function IngredientForm() {
//   const [addIngredient, { data, loading, error, reset }] =
//     useMutation(ADD_INGREDIENT);

//   async function handleSubmit(
//     values: IngredientValues,
//     {
//       setSubmitting,
//       setFieldError,
//     }: {
//       setSubmitting: (isSubmitting: boolean) => void;
//       setFieldError: (field: string, errorMsg: string) => void;
//     }
//   ) {
//     console.log("Submitting:", values);
//     try {
//       const response = await addIngredient({
//         variables: {
//           name: values.name,
//           extra_info: values.extra_info,
//           img: values.img instanceof File ? values.img : null,
//           alergens: values.alergens,
//           unit: values.unit,
//         },
//       });
//       console.log("Response:", response);
//     } catch (error: any) {
//       console.log(
//         "Error:",
//         error.graphQLErrors.map((err: any) => err.message)
//       );
//     }

//     // // If any erros, set them to their respective fields
//     // if (response.errors) {
//     //   console.log(response.errors);
//     // }

//     setSubmitting(false);
//   }

//   const initialValues: IngredientValues = {
//     name: "",
//     extra_info: "",
//     img: null,
//     alergens: [],
//     unit: "",
//   };

//   return (
//     <Formik
//       initialValues={initialValues}
//       validationSchema={Yup.object({
//         name: Yup.string().required("Zadajte názov"),
//         unit: Yup.string().required("Vyberte jednotku"),
//         extra_info: Yup.string(),
//       })}
//       onSubmit={handleSubmit}
//     >
//       {(props) => (
//         <Form className="m-2 grid grid-cols-2 items-center gap-2">
//           <Alert variant="danger" onClose={reset}>
//             <>
//               {error} - {error?.graphQLErrors.map((err) => err.message)}
//             </>
//           </Alert>
//           <div className="row-span-3">
//             <FileInput
//               label="Obrázok"
//               name="img"
//               // initial_url={
//               //   initial && initial.img && typeof initial.img === "string"
//               //     ? initial.img
//               //     : undefined
//               // }
//             />
//           </div>
//           <div>
//             <TextInput label="Názov" name="name" />
//           </div>
//           <div>
//             <TextInput label="Extra informácie" name="extra_info" />
//           </div>
//           <div>
//             <SelectInput
//               label="Jednotka"
//               name="unit"
//               query_options_schema={gql`
//                 query Units {
//                   units {
//                     id
//                     sign
//                   }
//                 }
//               `}
//               value_key="id"
//               label_key="sign"
//             />
//           </div>

//           <div className="col-span-2 md:col-span-1">
//             <MultiSelectInput
//               label="Alergeny"
//               name="alergens"
//               options={[
//                 { value: 1, label: "test" },
//                 { value: 2, label: "test2" },
//               ]}
//             />
//           </div>
//           <div className="col-span-2 grid place-content-center md:col-span-1">
//             <Button
//               variant="primary"
//               dark
//               type="submit"
//               disabled={props.isSubmitting || loading}
//             >
//               Vytvoriť
//             </Button>
//           </div>
//         </Form>
//       )}
//     </Formik>
//   );
// }

import { gql, useMutation } from "@apollo/client";
import { ApolloError, GraphQLErrors } from "@apollo/client/errors";

const ADD_INGREDIENT_MUTATION = gql`
  mutation AddIngredient(
    $name: String!
    $extra_info: String
    $img: Upload
    $alergens: [ID]
    $unit: ID!
  ) {
    createIngredient(
      input: {
        name: $name
        extraInfo: $extra_info
        img: $img
        alergens: $alergens
        unit: $unit
      }
    ) {
      ingredient {
        id
        name
        extraInfo
        img
        alergens {
          code
          name
        }
        unit {
          id
          name
        }
      }
    }
  }
`;

interface Alergen {
  id: string;
  name: string;
}

interface Unit {
  id: string;
  name: string;
}

export default function AddIngredientForm() {
  const [addIngredient, { loading, error }] = useMutation(
    ADD_INGREDIENT_MUTATION
  );
  const alergens: Alergen[] = [
    { id: "1", name: "alergen" },
    { id: "2", name: "alergen2" },
  ];

  const units: Unit[] = [
    { id: "1", name: "unit" },
    { id: "2", name: "unit2" },
  ];

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const formData = new FormData(form);
    try {
      const result = await addIngredient({ variables: formData });
      console.log(
        "Ingredient created:",
        result.data.createIngredient.ingredient
      );
    } catch (e: any) {
      // log all key value pairs of the error
      console.log("Error:", e);
      Object.keys(e).forEach((key) => {
        console.log(key, e[key]);
      });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">Name:</label>
      <input type="text" name="name" required />
      <label htmlFor="extra_info">Extra info:</label>
      <textarea name="extra_info"></textarea>
      <label htmlFor="img">Image:</label>
      <input type="file" name="img" accept="image/*" />
      <label htmlFor="alergens">Alergens:</label>
      <select name="alergens" multiple>
        {alergens.map((alergen) => (
          <option key={alergen.id} value={alergen.id}>
            {alergen.name}
          </option>
        ))}
      </select>
      <label htmlFor="unit">Unit:</label>
      <select name="unit" required>
        {units.map((unit) => (
          <option key={unit.id} value={unit.id}>
            {unit.name}
          </option>
        ))}
      </select>
      <button type="submit" disabled={loading}>
        Add Ingredient
      </button>
      {error && <p>Error adding ingredient: {error.message}</p>}
    </form>
  );
}
