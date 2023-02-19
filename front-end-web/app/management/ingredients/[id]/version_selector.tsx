"use client";

import Link from "next/link";
import { Menu, Transition } from "@headlessui/react";
import { Fragment } from "react";
import { ChevronDownIcon } from "@heroicons/react/20/solid";

import { usePathname } from "next/navigation";

import { IngredientVersion } from "./fetch_ingredient_detail";

export default function VersionSelector({
  ingredient_id,
  versions,
}: {
  ingredient_id: string;
  versions: IngredientVersion[];
}) {
  const pathname = usePathname();

  const currentVersion = versions.find((version) => version.url === pathname);

  return (
    <div className="relative">
      <Menu as="div" className="relative inline-block text-left">
        <div>
          <Menu.Button className="inline-flex w-full justify-center rounded-full bg-white px-3 py-1 text-sm shadow-md ">
            {/* Write the version number, which have the same url as the pathname */}
            {currentVersion
              ? "Verzia " + currentVersion.version_number
              : "Všeobecný prehľad"}
            <ChevronDownIcon
              className="ml-2 -mr-1 h-5 w-5 text-violet-200 hover:text-violet-100"
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
          <Menu.Items className="absolute right-0 mt-2 max-w-2xl origin-top divide-y divide-gray-100 overflow-auto rounded-xl bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div className="px-1 py-1">
              <Menu.Item>
                {({ active }) => (
                  <button
                    className={`${
                      active || !currentVersion ? "bg-primary" : ""
                    } group mb-1 flex w-full items-center justify-end rounded-lg px-2 py-2 text-right text-sm`}
                  >
                    Všeobecný prehľad
                  </button>
                )}
              </Menu.Item>
            </div>
            <div className="px-1 py-1">
              {versions.map((version) => (
                <Menu.Item key={version.version_number}>
                  {({ active }) => (
                    <Link
                      href={version.url}
                      className={`${
                        !active && currentVersion != version
                          ? version.is_active
                            ? "text-green-600"
                            : version.is_inactive
                            ? "text-yellow-400"
                            : version.is_deleted
                            ? "text-red-600"
                            : ""
                          : version.is_active
                          ? "bg-green-600 text-white"
                          : version.is_inactive
                          ? "bg-yellow-400 text-black"
                          : version.is_deleted
                          ? "bg-red-600 text-white"
                          : ""
                      } group mt-1 flex w-full items-center justify-end rounded-lg px-2 py-2 text-sm`}
                    >
                      Verzia - {version.version_number}
                    </Link>
                  )}
                </Menu.Item>
              ))}
            </div>
          </Menu.Items>
        </Transition>
      </Menu>
    </div>
  );
}
