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
    <div className="absolute top-0 right-0 z-10 -translate-y-1/2 ">
      <Menu as="div" className="relative inline-block text-left">
        <div>
          <Menu.Button
            className={`inline-flex w-full justify-center rounded-full px-3 py-1 text-sm shadow-md ${
              !currentVersion
                ? "bg-primary-200 text-primary-700"
                : currentVersion.is_active
                ? "bg-green-100 text-green-600"
                : currentVersion.is_inactive
                ? "bg-yellow-100 text-yellow-600"
                : currentVersion.is_deleted
                ? "bg-red-100 text-red-600"
                : ""
            }`}
          >
            {currentVersion
              ? "Verzia " + currentVersion.version_number
              : "Nová verzia"}
            <ChevronDownIcon
              className="ml-2 -mr-1 h-5 w-5 text-gray-600 hover:text-gray-400"
              aria-hidden="true"
            />
          </Menu.Button>
        </div>
        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <Menu.Items className="absolute -top-2 right-0 max-h-52 w-36 origin-bottom -translate-y-full divide-y divide-gray-200 overflow-auto rounded-xl bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div className="p-1">
              <Menu.Item>
                {({ active }) => (
                  <Link
                    href={`/management/ingredients/${ingredient.id}/new_version`}
                    className={`my-1 flex w-full items-center justify-end px-2 text-right text-sm`}
                  >
                    <PlusCircleIcon
                      className={`${
                        active || !current_id ? "text-primary-600" : ""
                      } h-6 w-6`}
                    />
                  </Link>
                )}
              </Menu.Item>
            </div>
            <div className="p-1">
              {versions.length > 0 ? (
                versions.map((version) => (
                  <Menu.Item key={version.version_number}>
                    {({ active }) => (
                      <Link
                        href={version.url}
                        className={`${
                          !active && currentVersion != version
                            ? version.is_active
                              ? "text-green-600"
                              : version.is_inactive
                              ? "text-yellow-600"
                              : version.is_deleted
                              ? "text-red-600"
                              : ""
                            : version.is_active
                            ? "bg-green-600 font-medium text-white"
                            : version.is_inactive
                            ? "bg-yellow-300 font-medium text-black"
                            : version.is_deleted
                            ? "bg-red-600 font-medium text-white"
                            : ""
                        } group mt-1 flex w-full items-center justify-end rounded-lg px-2 py-2 text-sm`}
                      >
                        Verzia - {version.version_number}
                      </Link>
                    )}
                  </Menu.Item>
                ))
              ) : (
                <p className="p-1 pr-2 text-end text-xs text-gray-600">
                  Žiadne verzie
                </p>
              )}
            </div>
          </Menu.Items>
        </Transition>
      </Menu>
    </div>
  );
}
