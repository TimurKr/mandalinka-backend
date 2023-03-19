"use client";

import Link from "next/link";
import { Menu, Transition } from "@headlessui/react";
import { Fragment } from "react";
import { ChevronDownIcon } from "@heroicons/react/20/solid";

import { PlusCircleIcon } from "@heroicons/react/24/outline";

import {
  IngredientDetail,
  IngredientVersion,
} from "@/components/fetching/ingredient_detail";
import Button from "@/components/button";

export default function VersionSelector({
  ingredient,
  current_id,
}: {
  ingredient: IngredientDetail;
  current_id?: number;
}) {
  const versions = ingredient.versions.sort(
    (a, b) => b.version_number - a.version_number
  );

  const currentVersion = versions.find((version) => version.id === current_id);

  if (!currentVersion && current_id) {
    console.log(currentVersion, current_id);
    return <p>NotFound</p>;
    // notFound();
  }

  return (
    <div className="flex w-full flex-nowrap gap-2 overflow-x-scroll p-2">
      <Button
        href={`/management/ingredients/${ingredient.id}/new_version`}
        variant="primary"
        className="w-auto grow-0 p-1"
        dark={!current_id}
        disabled={!current_id}
      >
        <PlusCircleIcon className="h-5 w-5" />
      </Button>
      {versions.map((version) => (
        <Button
          key={version.id}
          className="w-auto flex-none align-middle"
          href={version.url}
          variant={
            version.is_active
              ? "success"
              : version.is_inactive
              ? "warning"
              : version.is_deleted
              ? "danger"
              : "black"
          }
          dark={currentVersion?.id == version.id}
          disabled={currentVersion?.id == version.id}
        >
          Verzia - {version.version_number}
        </Button>
      ))}
    </div>
  );
}
