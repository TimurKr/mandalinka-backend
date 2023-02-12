"use client";

// import { useRouter } from "next/navigation";
// import { Fragment, useState } from "react";
// import { Listbox, Transition } from "@headlessui/react";
// import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";

interface Version {
  id: number;
  number: number;
  status: "active" | "inactive" | "deleted";
  url: string;
}

const versions = [
  {
    id: 30,
    number: 16,
    status: "inactive",
    url: "/management/ingredients/1/30",
  },
  {
    id: 29,
    number: 15,
    status: "inactive",
    url: "/management/ingredients/1/29",
  },
  { id: 28, number: 14, status: "active", url: "/management/ingredients/1/28" },
  {
    id: 27,
    number: 13,
    status: "deleted",
    url: "/management/ingredients/1/27",
  },
  {
    id: 26,
    number: 12,
    status: "deleted",
    url: "/management/ingredients/1/26",
  },
  {
    id: 25,
    number: 11,
    status: "deleted",
    url: "/management/ingredients/1/25",
  },
  {
    id: 24,
    number: 10,
    status: "deleted",
    url: "/management/ingredients/1/24",
  },
  { id: 23, number: 9, status: "deleted", url: "/management/ingredients/1/23" },
  { id: 22, number: 8, status: "deleted", url: "/management/ingredients/1/22" },
  {
    id: 21,
    number: 7,
    status: "deleted",
    url: "/management/ingredients/1/21",
  },
  { id: 20, number: 6, status: "deleted", url: "/management/ingredients/1/20" },
  { id: 19, number: 5, status: "deleted", url: "/management/ingredients/1/19" },
  { id: 18, number: 4, status: "deleted", url: "/management/ingredients/1/18" },
  { id: 17, number: 3, status: "deleted", url: "/management/ingredients/1/17" },
  { id: 16, number: 2, status: "deleted", url: "/management/ingredients/1/16" },
  { id: 15, number: 1, status: "deleted", url: "/management/ingredients/1/15" },
];

import Link from "next/link";
import { Menu, Transition } from "@headlessui/react";
import { Fragment } from "react";
import { ChevronDownIcon } from "@heroicons/react/20/solid";

import { usePathname } from "next/navigation";

export default function VersionSelector({
  ingrdient_id,
}: {
  ingrdient_id: string;
}) {
  const pathname = usePathname();

  const currentVersion = versions.find((version) => version.url === pathname);

  return (
    <div className="relative ml-2 inline">
      <Menu as="div" className="relative inline-block text-left">
        <div>
          <Menu.Button className="inline-flex w-full justify-center rounded-full bg-white px-3 py-1 text-sm shadow-md ">
            {/* Write the version number, which have the same url as the pathname */}
            {currentVersion
              ? "Verzia " + currentVersion.number
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
          <Menu.Items className="absolute right-0 mt-2 w-56 max-w-2xl origin-top-right divide-y divide-gray-100 overflow-auto rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div className="px-1 py-1">
              <Menu.Item>
                {({ active }) => (
                  <button
                    className={`${
                      active ? "bg-primary" : ""
                    } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                  >
                    Všeobecný prehľad
                  </button>
                )}
              </Menu.Item>
            </div>
            <div className="px-1 py-1">
              {versions.map((version) => (
                <Menu.Item key={version.id}>
                  {({ active }) => (
                    <Link
                      href={version.url}
                      className={`${
                        active ? "bg-primary" : ""
                      } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                    >
                      Verzia - {version.number}
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
