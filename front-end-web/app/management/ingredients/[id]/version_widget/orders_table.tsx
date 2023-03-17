"use client";

import Alert from "@/components/alert";
import ConfirmationModal from "@/components/confirmation_modal";
import { IngredientVersion } from "@/components/fetching/ingredient_detail";
import { Unit } from "@/components/fetching/units";
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
import { useRef, useState } from "react";

export default function OrdersTable({
  data,
  modify_url,
}: {
  data: IngredientVersion;
  modify_url: string;
}) {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [confirmDeliveredID, setConfirmDeliveredID] = useState<number | null>(
    null
  );
  const [confirmUndeliveredID, setConfirmUndeliveredID] = useState<
    number | null
  >(null);
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

  async function setOrdered(id: number | null, state: boolean) {
    if (id === null) return;

    const formData = new FormData();
    formData.append("is_delivered", state.toString());

    const response = await fetch(modify_url + id.toString() + "/", {
      method: "PATCH",
      body: formData,
    })
      .then((response) => {
        setConfirmDeliveredID(null);
        setConfirmUndeliveredID(null);
        if (response.ok) setTimeout(router.refresh, 500);
        else {
          return response.json();
        }
      })
      .catch((error) => {
        console.log("Error: ", error);
        setConfirmDeliveredID(null);
        setConfirmUndeliveredID(null);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      });
  }

  async function changeExpiration(id: number | null, date: Date) {
    if (id === null) return;

    const formData = new FormData();
    formData.append("expiration_date", date.toISOString().split("T")[0]);

    const response = await fetch(modify_url + id.toString() + "/", {
      method: "PATCH",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          setChangeExpirationID(null);
          setTimeout(router.refresh, 500);
        } else {
          return response.json();
        }
      })
      .catch((error) => {
        console.log("Error: ", error);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      });
  }

  async function setExpired(id: number | null, state: boolean) {
    if (id === null) return;

    const formData = new FormData();
    formData.append("is_expired", state.toString());

    const response = await fetch(modify_url + id.toString() + "/", {
      method: "PATCH",
      body: formData,
    })
      .then((response) => {
        setConfirmExpiredID(null);
        if (response.ok) setTimeout(router.refresh, 500);
        else {
          return response.json();
        }
      })
      .catch((error) => {
        console.log("Error: ", error);
        setConfirmExpiredID(null);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      });
  }

  return (
    <>
      {/* Confirm delivered */}
      <ConfirmationModal
        show={confirmDeliveredID !== null}
        onClose={() => setConfirmDeliveredID(null)}
        onConfirm={() => setOrdered(confirmDeliveredID, true)}
        confirmText="Potvrdiť"
        header="Potvrdiť doručenie"
        version="success"
      ></ConfirmationModal>
      {/* Confirm undelivered */}
      <ConfirmationModal
        show={confirmUndeliveredID !== null}
        onClose={() => setConfirmUndeliveredID(null)}
        onConfirm={() => setOrdered(confirmUndeliveredID, false)}
        confirmText="Potvrdiť"
        header="Potvrdiť nedoručenie"
      ></ConfirmationModal>
      {/* Change expiration date */}
      <ConfirmationModal
        show={changeExpirationID !== null}
        onClose={() => setChangeExpirationID(null)}
        onConfirm={() => expirationFormRef.current?.submitForm()}
        confirmText="Potvrdiť"
        header="Zmeniť dátum expirácie"
      >
        <Formik
          innerRef={expirationFormRef}
          initialValues={{
            expiration_date: new Date(
              data.orders.find((o) => o.id === changeExpirationID)
                ?.expiration_date || new Date()
            ),
          }}
          onSubmit={(values) => {
            changeExpiration(
              changeExpirationID,
              new Date(values.expiration_date)
            );
          }}
        >
          <DateTimeInput label="Nový dátum expirácie" name="expiration_date" />
        </Formik>
      </ConfirmationModal>
      <ConfirmationModal
        show={confirmExpiredID !== null}
        onClose={() => setConfirmExpiredID(null)}
        onConfirm={() =>
          setExpired(
            confirmExpiredID,
            data.orders.find((o) => o.id === confirmExpiredID)?.is_expired
              ? false
              : true
          )
        }
        confirmText="Potvrdiť"
        header={
          data.orders.find((o) => o.id === confirmExpiredID)?.is_expired
            ? "Zrušiť expiráciu"
            : "Potvrdiť expiráciu"
        }
      ></ConfirmationModal>

      {errorMessage && (
        <Alert onClose={() => setErrorMessage(null)} version="danger">
          {errorMessage}
        </Alert>
      )}
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
                    : new Date(order.expiration_date) < new Date()
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
                  <p
                    className="cursor-pointer hover:underline"
                    onClick={() => setChangeExpirationID(order.id)}
                  >
                    {order.expiration_date}
                  </p>
                  {!order.is_expired ? (
                    <TrashIcon
                      className="text-danger hover:bg-danger/10 h-5 w-5 cursor-pointer rounded-full"
                      onClick={() => setConfirmExpiredID(order.id)}
                    />
                  ) : (
                    <ArrowUturnLeftIcon
                      className="text-success hover:bg-success/10 h-5 w-5 cursor-pointer rounded-full"
                      onClick={() => setConfirmExpiredID(order.id)}
                    />
                  )}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.amount} {order.unit.sign}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.cost} €
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {order.is_delivered ? (
                    <button
                      onClick={() => {
                        setConfirmUndeliveredID(order.id);
                      }}
                    >
                      <Tooltip content="Označiť ako nedoručené">
                        <ArrowRightOnRectangleIcon className="text-danger h-5 w-5" />
                      </Tooltip>
                    </button>
                  ) : (
                    <button
                      onClick={() => {
                        setConfirmDeliveredID(order.id);
                      }}
                    >
                      <Tooltip content="Označiť ako doručené">
                        <ArrowLeftOnRectangleIcon className="text-success h-5 w-5" />
                      </Tooltip>
                    </button>
                  )}
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
