"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navigation() {
  const pathname = usePathname();

  console.log(pathname);

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
    if (pathname == page.href) {
      page.active = true;
    }
  });

  return (
    <nav className="flex h-full flex-col justify-center">
      {pages.map((page) => (
        <Link
          key={page.title}
          href={page.href}
          className={`${page.active ? "active" : ""}`}
        >
          <span className="material-symbols-outlined">{page.icon}</span>
        </Link>
      ))}
    </nav>
  );
}
