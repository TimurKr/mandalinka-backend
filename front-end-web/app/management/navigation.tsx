"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navigation() {
  const pathname = usePathname();

  const pages = [
    {
      title: "Menu",
      href: "/management/menus",
      icon: "menu_book",
      active: false,
    },
    {
      title: "Recepty",
      href: "/management/recipes",
      icon: "ramen_dining",
      active: false,
    },
    {
      title: "Suroviny",
      href: "/management/ingredients",
      icon: "egg_alt",
      active: false,
    },
  ];

  pages.forEach((page) => {
    if (pathname && pathname.startsWith(page.href)) {
      page.active = true;
    }
  });

  return (
    <nav className="group flex h-full flex-col justify-center p-2">
      {pages.map((page) => (
        <Link
          key={page.title}
          href={page.href}
          className={`relative my-1 grid h-10 w-10  place-content-center rounded-xl p-1 text-2xl md:text-3xl ${
            page.active
              ? "bg-primary cursor-default border font-semibold"
              : "hover:bg-primary/50 active:bg-primary/70 font-extralight shadow-md hover:shadow-xl"
          }`}
        >
          <span
            className={`material-symbols-outlined text-2xl md:text-3xl ${
              page.active ? "font-semibold text-black" : "font-extralight"
            }`}
          >
            {page.icon}
          </span>
          <div className="bg-primary invisible absolute top-1/2 ml-14 -translate-y-1/2 rounded-md p-2 text-sm opacity-0 transition group-hover:visible group-hover:opacity-100">
            {page.title}
          </div>
        </Link>
      ))}
    </nav>
  );
}
