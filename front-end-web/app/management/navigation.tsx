"use client";

import Link from "next/link";

export default function Navigation() {
  return (
    <nav>
      <Link href="/management/menus"> Menus </Link>
      <Link href="/management/recipes"> Recepty </Link>
      <Link href="/management/ingredients"> Ingrediencie </Link>
    </nav>
  );
}
