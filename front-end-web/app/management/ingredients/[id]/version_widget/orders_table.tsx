"use client";

import Alert from "@/components/alert";
import ConfirmationModal from "@/components/confirmation_modal";
import {
  IngredientVersion,
  Order,
} from "@/components/fetching/ingredient_detail";
import DateTimeInput from "@/components/form_elements/date_time";
import parseInvalidResponse from "@/components/form_elements/parse_invalid_response";
import {
  ArrowLeftOnRectangleIcon,
  ArrowRightOnRectangleIcon,
  ArrowUturnLeftIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";
import { Table, Tooltip } from "flowbite-react";
import { Formik, FormikProps } from "formik";
import { useRouter } from "next/navigation";
import { startTransition, useRef, useState, useTransition } from "react";

function ToggleDelivered({
  modify_url,
  order,
}: {
  modify_url: string;
  order: Order;
}) {
  if (order.is_delivered && order.amount !== order.in_stock_amount)
    return <></>;

  const [state, setState] = useState<boolean | null>(null);
  const formRef = useRef<FormikProps<any>>(null);

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [isSubmitting, setIsSubmitting] = useState(false);

  async function sendData(date: Date) {
    if (state === null) return;

    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("is_delivered", state.toString());
    formData.append("delivery_date", date.toISOString());

    await fetch(modify_url + order.id.toString() + "/", {
      method: "PATCH",
      body: formData,
    }).then((response) => {
      parseInvalidResponse(
        response,
        (field, errorMsg) =>
          setErrorMessage(errorMessage + "\n" + field + ": " + errorMsg),
        setErrorMessage,
        true
      );
      setIsSubmitting(false);
    });
  }

  return (
    <>
      {/* Confirm delivered or undelivered */}
      <ConfirmationModal
        show={state !== null}
        onClose={() => setState(null)}
        onConfirm={() => formRef.current?.submitForm()}
        confirmText="Potvrdiť"
        header={state ? "Potvďte doručenie" : "Potvďte vrátenie"}
        variant={state ? "success" : "danger"}
        disableConfirm={isSubmitting}
      >
        <Alert onClose={() => setErrorMessage(null)} variant="danger">
          {errorMessage}
        </Alert>

        <Formik
          innerRef={formRef}
          initialValues={{
            delivery_date: new Date(),
          }}
          onSubmit={(values) => {
            sendData(new Date(values.delivery_date));
          }}
        >
          <DateTimeInput label="Dátum doručenia" name="delivery_date" time />
        </Formik>
      </ConfirmationModal>
      {order.is_delivered ? (
        <button
          onClick={() => {
            setState(!order.is_delivered);
          }}
        >
          <ArrowRightOnRectangleIcon className="text-danger h-5 w-5" />
        </button>
      ) : (
        <button
          onClick={() => {
            setState(!order.is_delivered);
          }}
        >
          <ArrowLeftOnRectangleIcon className="text-success h-5 w-5" />
        </button>
      )}
    </>
  );
}

function DeleteOrder({
  modify_url,
  order,
}: {
  modify_url: string;
  order: Order;
}) {
  if (order.amount !== order.in_stock_amount) return <></>;
  const [confirmDeleteModal, setConfirmDeleteModal] = useState<boolean>(false);

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [isSubmitting, setIsSubmitting] = useState(false);

  async function deleteOrder() {
    setIsSubmitting(true);
    fetch(modify_url + order.id.toString() + "/", {
      method: "DELETE",
    })
      .then((response) =>
        parseInvalidResponse(
          response,
          (field, errorMsg) =>
            setErrorMessage(errorMessage + "\n" + field + ": " + errorMsg),
          setErrorMessage,
          true
        )
      )
      .catch((error) => {
        console.log("Error: ", error);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      })
      .finally(() => setIsSubmitting(false));
  }

  return (
    <>
      <ConfirmationModal
        show={confirmDeleteModal}
        onClose={() => setConfirmDeleteModal(false)}
        onConfirm={deleteOrder}
        confirmText="Potvrdiť"
        header="Potvďte zmazanie"
        variant="danger"
        disableConfirm={isSubmitting}
      >
        <Alert onClose={() => setErrorMessage(null)} variant="danger">
          {errorMessage}
        </Alert>
        <p>
          Naozaj chcete zmazať objednávku {order.id}? Táto akcia je nevratná.
        </p>
      </ConfirmationModal>
      <button
        onClick={() => {
          setConfirmDeleteModal(true);
        }}
      >
        <TrashIcon className="text-danger h-5 w-5" />
      </button>
    </>
  );
}

function ActionsCell({
  modify_url,
  order,
}: {
  modify_url: string;
  order: Order;
}) {
  return (
    <>
      <ToggleDelivered modify_url={modify_url} order={order} />
      <DeleteOrder modify_url={modify_url} order={order} />
    </>
  );
}

function ExpirationCell({
  modify_url,
  order,
}: {
  modify_url: string;
  order: Order;
}) {
  const router = useRouter();
  const [changeExpirationModal, setChangeExpirationModal] =
    useState<boolean>(false);
  const expirationFormRef = useRef<FormikProps<any>>(null);
  const [confirmExpiredModal, setConfirmExpiredModal] =
    useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function changeExpiration(date: Date) {
    const formData = new FormData();
    formData.append("expiration_date", date.toISOString().split("T")[0]);

    await fetch(modify_url + order.id.toString() + "/", {
      method: "PATCH",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          return startTransition(() => window.location.reload());
        } else {
          return response.json();
        }
      })
      .catch((error) => {
        console.log("Error: ", error);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      });
  }

  async function setExpired() {
    const formData = new FormData();
    formData.append("is_expired", "true");

    await fetch(modify_url + order.id.toString() + "/", {
      method: "PATCH",
      body: formData,
    })
      .then((response) => {
        if (response.ok) window.location.reload();
        else {
          return response.json();
        }
      })
      .catch((error) => {
        console.log("Error: ", error);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      });
  }

  return (
    <>
      <ConfirmationModal
        show={changeExpirationModal}
        onClose={() => setChangeExpirationModal(false)}
        onConfirm={() => expirationFormRef.current?.submitForm()}
        confirmText="Potvrdiť"
        header="Zmeniť dátum expirácie"
      >
        <Alert onClose={() => setErrorMessage(null)} variant="danger">
          {errorMessage}
        </Alert>
        <Formik
          innerRef={expirationFormRef}
          initialValues={{
            expiration_date: new Date(order.expiration_date),
          }}
          onSubmit={(values) => {
            changeExpiration(new Date(values.expiration_date));
          }}
        >
          <DateTimeInput label="Nový dátum expirácie" name="expiration_date" />
        </Formik>
      </ConfirmationModal>
      <ConfirmationModal
        show={confirmExpiredModal}
        onClose={() => setConfirmExpiredModal(false)}
        onConfirm={setExpired}
        confirmText="Potvrdiť"
        header={"Potvrdiť expiráciu"}
      >
        <Alert onClose={() => setErrorMessage(null)} variant="danger">
          {errorMessage}
        </Alert>
        <p>Ako dátum sa použije {order.expiration_date}</p>
        <p>Táto akcia sa dá vrátiť iba vymazaním vytvoreného odpisu.</p>
      </ConfirmationModal>
      {order.is_expired ? (
        <p>{order.expiration_date}</p>
      ) : (
        <a
          className="cursor-pointer hover:underline"
          onClick={() => setChangeExpirationModal(true)}
        >
          {order.expiration_date}
        </a>
      )}
      {!order.is_expired && order.is_delivered && (
        <TrashIcon
          className="text-danger hover:bg-danger/10 h-5 w-5 cursor-pointer rounded-full"
          onClick={() => setConfirmExpiredModal(true)}
        />
      )}
    </>
  );
}

export default function OrdersTable({
  data,
  modify_url,
}: {
  data: IngredientVersion;
  modify_url: string;
}) {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [changeExpirationID, setChangeExpirationID] = useState<number | null>(
    null
  );
  const expirationFormRef = useRef<FormikProps<any>>(null);

  const [confirmExpiredID, setConfirmExpiredID] = useState<number | null>(null);

  const router = useRouter();

  // Sort orders by undeliverd first and then by delivery date
  data.orders.sort((a, b) => {
    if (a.is_delivered === b.is_delivered) {
      return new Date(a.delivery_date) > new Date(b.delivery_date) ? -1 : 1;
    } else {
      return a.is_delivered ? 1 : -1;
    }
  });
  const [orders, setOrders] = useState(data.orders.slice(0, 2));

  function showAllOrders() {
    setOrders(data.orders);
  }

  function hideAllOrders() {
    setOrders(data.orders.slice(0, 2));
  }

  return (
    <>
      <Alert onClose={() => setErrorMessage(null)} variant="danger">
        {errorMessage}
      </Alert>
      {orders.length > 0 ? (
        <Table className="w-full table-auto pt-1">
          <Table.Head className="w-full justify-between text-xs uppercase">
            <Table.HeadCell className="!p-1 text-center">
              Dátum objednávky
            </Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">
              Dátum doručenia
            </Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">
              Expirácia
            </Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">
              Množstvo
            </Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">
              Na sklade
            </Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">Cena</Table.HeadCell>
            <Table.HeadCell>
              <span className="sr-only !p-1">Edit</span>
            </Table.HeadCell>
          </Table.Head>
          <Table.Body>
            {orders.map((order, index) => (
              <Table.Row
                key={index}
                className={`${
                  !order.is_delivered
                    ? "bg-warning/10"
                    : new Date(order.expiration_date) < new Date() ||
                      order.is_expired
                    ? "bg-danger/10"
                    : ""
                }`}
              >
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.order_date}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.delivery_date}
                </Table.Cell>
                <Table.Cell className="flex items-center justify-center !p-1 text-center text-sm">
                  <ExpirationCell modify_url={modify_url} order={order} />
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.amount} {order.unit.sign}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.in_stock_amount} {order.unit.sign}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.cost} €
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  <ActionsCell modify_url={modify_url} order={order} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      ) : (
        <p className="w-full text-center text-sm text-gray-500">
          Žiadne objednávky
        </p>
      )}
      <div className="flex justify-between">
        {orders.length == 2 && data.orders.length > 2 ? (
          <a
            onClick={showAllOrders}
            className="w-full cursor-pointer pt-1 text-center text-sm text-gray-600 hover:underline"
          >
            Zobraziť všetky
          </a>
        ) : orders.length > 2 ? (
          <a
            onClick={hideAllOrders}
            className="w-full cursor-pointer pt-1 text-center text-sm text-gray-600 hover:underline"
          >
            Zobraziť menej
          </a>
        ) : null}
      </div>
    </>
  );
}
