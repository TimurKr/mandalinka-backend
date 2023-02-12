"use client";

import Link from "next/link";

export default function Navigation() {
  const pages = [
    ["Účet", "/account"],
    ["Management", "/management"],
    ["Login", "/login"],
  ];

  return (
    <nav
      className="sticky top-0 flex justify-between py-2 backdrop-blur"
      role="navigation"
    >
      <Link href="/">tangerine</Link>
      <ol className="flex flex-col items-center sm:flex-row">
        {pages.map(([name, href]) => (
          <li className="py-2 px-2" key={name}>
            <Link
              href={href}
              className="rounded-xl bg-transparent p-2 hover:bg-white hover:bg-opacity-10 hover:shadow-md"
            >
              {name}
            </Link>
          </li>
        ))}
      </ol>
    </nav>
  );
}
