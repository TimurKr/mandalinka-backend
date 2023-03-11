"use client";

import Button from "@/components/button";
import { IngredientVersion } from "@/components/fetching/ingredient_detail";
import { Unit } from "@/components/fetching/units";
import { MinusIcon, PlusIcon } from "@heroicons/react/24/outline";
import { Dropdown, Modal } from "flowbite-react";
import dynamic from "next/dynamic";
import { lazy, Suspense, useEffect, useState } from "react";

export default function InStockManipulation({
  data,
  units,
}: {
  data: IngredientVersion;
  units: Unit[];
}) {
  const [showRemoveModal, setRemoveModal] = useState(false);
  const [showOrderModal, setOrderModal] = useState(false);
  const [isShowing, setIsShowing] = useState(true);

  const RemoveModal = dynamic(() => import("./remove_stock_modal"), {
    ssr: false,
  });

  return (
    <>
      <div className="flex h-full items-center">
        <RemoveModal
          show={showRemoveModal}
          onClose={() => setRemoveModal(false)}
          units={units}
        />

        <Button
          color="danger"
          onClick={() => setRemoveModal(true)}
          className="!p-2"
        >
          <MinusIcon className="h-3 w-3" />
        </Button>
        <p className="shrink-0 px-3">
          {data.in_stock_amount}{" "}
          {units.find((unit) => unit.id === data.unit)?.sign || "Wrong unit"}
        </p>
        <Button
          color="success"
          onClick={() => setOrderModal(true)}
          className="!p-2"
        >
          <PlusIcon className="h-3 w-3" />
        </Button>
      </div>
    </>
  );
}
