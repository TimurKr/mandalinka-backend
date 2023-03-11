import Button from "@/components/button";
import { Unit } from "@/components/fetching/units";
import NumberInput from "@/components/form_elements/number";
import Select from "@/components/form_elements/select";
import TextInput from "@/components/form_elements/text";
import { FaceSmileIcon } from "@heroicons/react/24/outline";
import { Modal } from "flowbite-react";
import { Form, Formik } from "formik";
import dynamic from "next/dynamic";
import * as Yup from "yup";

export default function RemoveModal({
  show,
  units,
  onClose,
}: {
  show: boolean;
  units: Unit[];
  onClose: () => void;
}) {
  async function handleSubmit(
    values: any,
    { setSubmitting }: { setSubmitting: (isSubmitting: boolean) => void }
  ) {
    console.log(values);
  }

  return (
    <Modal dismissible={true} show={show} onClose={onClose} size="md">
      <Modal.Header>Odoberte množstvo zo skladu</Modal.Header>
      <Modal.Body>
        <Formik
          initialValues={{ amount: 0, unit: 0, reason: "", description: "" }}
          onSubmit={handleSubmit}
          validationSchema={Yup.object().shape({
            amount: Yup.number()
              .required("Required")
              .min(0, "Zadajte kladné číslo"),
            unit: Yup.number().required("Required"),
            reason: Yup.string().required("Required"),
            description: Yup.string().when("reason", {
              is: "other",
              then: () => Yup.string().required("Required"),
            }),
          })}
        >
          <Form className="flex flex-wrap gap-2">
            <div className="flex-auto">
              <NumberInput
                disabled
                name="amount"
                label="Množstvo"
                className="flex-auto"
              />
            </div>
            <div className="flex-auto">
              <Select
                name="unit"
                label="Jednotka"
                options={units.map((unit) => ({
                  value: unit.id,
                  label: unit.name,
                }))}
              />
            </div>
            <div className="flex-auto shrink-0">
              <Select
                name="reason"
                label="Dôvod"
                options={[
                  { value: "expired", label: "Expirovalo" },
                  { value: "went_bad", label: "Pokazilo sa pred expiráciou" },
                  { value: "other", label: "Iné" },
                ]}
              />
            </div>
            <div className="flex-auto shrink-0">
              <TextInput name="description" label="Popis" />
            </div>
          </Form>
        </Formik>
      </Modal.Body>
      <Modal.Footer>
        <Button color="primary" dark onClick={onClose}>
          I accept
        </Button>
        <Button color="secondary" onClick={onClose}>
          Decline
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
