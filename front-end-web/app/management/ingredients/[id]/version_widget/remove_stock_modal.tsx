import Alert from "@/components/alert";
import Button from "@/components/button";
import { IngredientVersion } from "@/components/fetching/ingredient_detail";
import { Unit } from "@/components/fetching/units";
import NumberInput from "@/components/form_elements/number";
import parseInvalidResponse from "@/components/form_elements/parse_invalid_response";
import Select from "@/components/form_elements/select";
import TextInput from "@/components/form_elements/text";
import { Modal } from "flowbite-react";
import { Form, Formik } from "formik";
import { useRouter } from "next/navigation";
import { useState } from "react";
import * as Yup from "yup";

export default function RemoveModal({
  show,
  units,
  onClose,
  ingredientVersion,
  submit_url,
  router,
}: {
  show: boolean;
  units: Unit[];
  onClose: () => void;
  ingredientVersion: IngredientVersion;
  submit_url: string;
  router: ReturnType<typeof useRouter>;
}) {
  const [all, setAll] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(
    values: any,
    {
      setSubmitting,
      setFieldError,
    }: {
      setSubmitting: (isSubmitting: boolean) => void;
      setFieldError: (field: string, errorMsg: string) => void;
    }
  ) {
    const formValues = new FormData();
    formValues.append("ingredient_version", ingredientVersion.id.toString());
    formValues.append("amount", values.amount);
    formValues.append("unit", values.unit.toString());
    formValues.append("reason", values.reason);
    formValues.append("description", values.description);

    const response = await fetch(submit_url, {
      method: "POST",
      body: formValues,
    }).then((response) => {
      if (response.status === 400) {
        parseInvalidResponse(response, setFieldError, setErrorMessage);
      }
      return response;
    });
  }

  return (
    <Modal dismissible={true} show={show} onClose={onClose} size="md">
      <Modal.Header>Odoberte zo skladu</Modal.Header>
      <Modal.Body>
        {errorMessage && (
          <Alert
            version="danger"
            className="!mb-3"
            onClose={() => setErrorMessage(null)}
          >
            {errorMessage}
          </Alert>
        )}
        <Formik
          initialValues={{
            amount: 0,
            unit: ingredientVersion.unit.id,
            reason: "",
            description: "",
            all: false,
          }}
          onSubmit={handleSubmit}
          validationSchema={Yup.object().shape({
            amount: Yup.number()
              .required("Required")
              .min(0, "Zadajte kladné číslo"),
            // .max(ingredientVersion.in_stock_amount, "Nedostatok množstva"),
            unit: Yup.number().required("Required"),
            reason: Yup.string().required("Required"),
            description: Yup.string().when("reason", {
              is: "other",
              then: () => Yup.string().required("Required"),
            }),
          })}
        >
          {(props) => (
            <Form className="flex flex-wrap items-center gap-2">
              <div className="flex-auto">
                <NumberInput name="amount" label="Množstvo" disabled={all} />
              </div>
              <div className="flex-auto">
                <Select
                  name="unit"
                  label="Jednotka"
                  options={units.map((unit) => ({
                    value: unit.id,
                    label: unit.name,
                  }))}
                  disabled={all}
                />
              </div>
              <div className="flex flex-auto items-center">
                <input
                  id="all-checkbox"
                  type="checkbox"
                  className="text-primary focus:outline-primary focus:ring-primary rounded"
                  onChange={(event) => {
                    setAll(event.target.checked);
                    props.setFieldValue(
                      "amount",
                      ingredientVersion.in_stock_amount
                    );
                    props.setFieldValue("unit", ingredientVersion.unit.id);
                  }}
                />
                <label
                  htmlFor="all-checkbox"
                  className="px-2 text-sm text-gray-700"
                >
                  Všetko na sklade
                </label>
              </div>
              <div className="flex-auto shrink-0">
                <Select
                  name="reason"
                  label="Zadajte dôvod"
                  options={[
                    { value: "expired", label: "Expirovalo" },
                    { value: "went_bad", label: "Pokazilo sa pred expiráciou" },
                    { value: "other", label: "Iné" },
                  ]}
                />
              </div>
              <div className="flex-auto shrink-0">
                <TextInput name="description" label="Poznámka" />
              </div>
              <div className="flex-auto">
                <Button
                  type="submit"
                  color="primary"
                  dark
                  disabled={props.isSubmitting}
                >
                  Odobrať
                </Button>
              </div>
            </Form>
          )}
        </Formik>
      </Modal.Body>
    </Modal>
  );
}
