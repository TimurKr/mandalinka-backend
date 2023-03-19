"use client";

import Alert from "@/components/alert";
import { IngredientVersion } from "@/components/fetching/ingredient_detail";
import { Unit } from "@/components/fetching/units";
import parseInvalidResponse from "@/components/form_elements/parse_invalid_response";
import ConfirmationModal from "@/components/confirmation_modal";
import {
  ArrowLeftOnRectangleIcon,
  ArrowRightOnRectangleIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";
import { Modal, Table, Tooltip } from "flowbite-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function RemovalsTable({
  data,
  delete_url,
}: {
  data: IngredientVersion;
  delete_url: string;
}) {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [deleteID, setDeleteID] = useState<number | null>(null);

  const router = useRouter();

  async function deleteRemoval(id: number | null) {
    if (id === null) return;

    const response = await fetch(delete_url + id.toString() + "/", {
      method: "DELETE",
    })
      .then((response) => {
        setDeleteID(null);
        if (response.ok) {
          window.location.reload();
        } else {
          return response.json();
        }
      })
      .catch((error) => {
        console.log("Error: ", error);
        setErrorMessage("Nastala chyba pri spracovaní odpovede zo servera");
      });
  }

  // Sort removals by date
  data.removals.sort((a, b) => {
    return new Date(a.date) > new Date(b.date) ? -1 : 1;
  });
  const [removals, setRemovals] = useState(data.removals.slice(0, 2));

  function showAllRemovals() {
    setRemovals(data.removals);
  }

  function hideAllRemovals() {
    setRemovals(data.removals.slice(0, 2));
  }

  return (
    <>
      <ConfirmationModal
        show={deleteID !== null}
        onClose={() => setDeleteID(null)}
        onConfirm={() => deleteRemoval(deleteID)}
        header="Naozaj chcete odstrániť tento záznam?"
        confirmText="Odstrániť"
      >
        Táto akcia je nevratná.
      </ConfirmationModal>
      <Alert onClose={() => setErrorMessage(null)} variant="danger">
        {errorMessage}
      </Alert>
      {removals.length > 0 ? (
        <Table className="w-full table-auto pt-1">
          <Table.Head className="w-full justify-between text-xs uppercase">
            <Table.HeadCell className="!p-1 text-center">Dátum</Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">
              Množstvo
            </Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">Dôvod</Table.HeadCell>
            <Table.HeadCell className="!p-1 text-center">Info</Table.HeadCell>
            <Table.HeadCell>
              <span className="sr-only !p-1">Edit</span>
            </Table.HeadCell>
          </Table.Head>
          <Table.Body>
            {removals.map((removal, index) => (
              <Table.Row key={index}>
                <Table.Cell className="!p-1 text-center text-sm">
                  {removal.date}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {removal.amount} {removal.unit.sign}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {removal.reason}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  {removal.description}
                </Table.Cell>
                <Table.Cell className="!p-1 text-center text-sm">
                  <button
                    onClick={() => {
                      setDeleteID(removal.id);
                    }}
                  >
                    <TrashIcon className="text-danger h-5 w-5" />
                  </button>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      ) : (
        <p className="w-full text-center text-sm text-gray-500">
          Žiadne odpisy
        </p>
      )}
      <div className="flex justify-between">
        {removals.length == 2 && data.removals.length > 2 ? (
          <a
            onClick={showAllRemovals}
            className="w-full cursor-pointer pt-1 text-center text-sm text-gray-600 hover:underline"
          >
            Zobraziť všetky
          </a>
        ) : removals.length > 2 ? (
          <a
            onClick={hideAllRemovals}
            className="w-full cursor-pointer pt-1 text-center text-sm text-gray-600 hover:underline"
          >
            Zobraziť menej
          </a>
        ) : null}
      </div>
    </>
  );
}
