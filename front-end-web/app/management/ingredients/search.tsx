"use client";

import { useState } from "react";
import { FixedSizeList as List } from "react-window";
import { usePathname } from "next/navigation";

import Fuse from "fuse.js";

import Link from "next/link";
import { useRouter } from "next/navigation";

interface Ingredient {
  name: string;
  id: number;
  used_last_month: number;
}

const ingredients = [
  {
    name: "Mlieko",
    id: 1,
    used_last_month: 10,
    url: "/management/ingredients/1",
  },
  {
    name: "Maslo",
    id: 2,
    used_last_month: 5,
    url: "/management/ingredients/2",
  },
  {
    name: "Jogurt",
    id: 3,
    used_last_month: 3,
    url: "/management/ingredients/3",
  },
  {
    name: "Smotana",
    id: 4,
    used_last_month: 24,
    url: "/management/ingredients/4",
  },
  {
    name: "Cukor",
    id: 5,
    used_last_month: 2,
    url: "/management/ingredients/5",
  },
  { name: "Múka", id: 6, used_last_month: 1, url: "/management/ingredients/6" },
  {
    name: "Vajcia",
    id: 7,
    used_last_month: 0,
    url: "/management/ingredients/7",
  },
  {
    name: "Parmezán",
    id: 8,
    used_last_month: 11,
    url: "/management/ingredients/8",
  },
  {
    name: "Korenie",
    id: 9,
    used_last_month: 0,
    url: "/management/ingredients/9",
  },
  {
    name: "Hliva",
    id: 10,
    used_last_month: 13,
    url: "/management/ingredients/10",
  },
  {
    name: "Kapusta",
    id: 11,
    used_last_month: 15,
    url: "/management/ingredients/11",
  },
  {
    name: "Cibuľa",
    id: 12,
    used_last_month: 12,
    url: "/management/ingredients/12",
  },
  {
    name: "Celer",
    id: 13,
    used_last_month: 11,
    url: "/management/ingredients/13",
  },
  {
    name: "Kuracie maso",
    id: 14,
    used_last_month: 13,
    url: "/management/ingredients/14",
  },
  {
    name: "Hovädzie maso",
    id: 15,
    used_last_month: 12,
    url: "/management/ingredients/15",
  },
  {
    name: "Slanina",
    id: 16,
    used_last_month: 11,
    url: "/management/ingredients/16",
  },
  {
    name: "Šunka",
    id: 17,
    used_last_month: 10,
    url: "/management/ingredients/17",
  },
  {
    name: "Klobása",
    id: 18,
    used_last_month: 9,
    url: "/management/ingredients/18",
  },
  {
    name: "Kuřecí prsíčka",
    id: 19,
    used_last_month: 8,
    url: "/management/ingredients/19",
  },
  {
    name: "Hovězí dobré papko prsíčka",
    id: 20,
    used_last_month: 7,
    url: "/management/ingredients/20",
  },
  {
    name: "Kuřecí maso",
    id: 21,
    used_last_month: 6,
    url: "/management/ingredients/21",
  },
  {
    name: "Hovězí maso",
    id: 22,
    used_last_month: 5,
    url: "/management/ingredients/22",
  },
  {
    name: "Kuřecí křídla",
    id: 23,
    used_last_month: 4,
    url: "/management/ingredients/23",
  },
  {
    name: "Hovězí křídla",
    id: 24,
    used_last_month: 3,
    url: "/management/ingredients/24",
  },
];

const fuse = new Fuse(ingredients, { keys: ["name", "id"] });

export default function Search() {
  const [search, setSearch] = useState("");
  const [matchingIngredients, setMatchingIngredients] = useState(
    ingredients.slice().sort((a, b) => b.used_last_month - a.used_last_month)
  );

  const router = useRouter();

  function handleSearch(event: React.ChangeEvent<HTMLInputElement>): void {
    setSearch(event.target.value);

    let results = fuse.search(event.target.value).map((result) => result.item);
    if (results.length === 0) {
      results = ingredients
        .slice()
        .sort((a, b) => b.used_last_month - a.used_last_month);
    }

    setMatchingIngredients(results);
  }

  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>): void {
    event.preventDefault();
    router.push(matchingIngredients[0].url);
  }

  const path = usePathname();

  return (
    <div className="relative h-full w-[15rem] flex-col">
      <List
        height={window.innerHeight}
        itemCount={matchingIngredients.length}
        itemSize={35}
        width={"100%"}
        className="overflow-x-visible overscroll-auto"
      >
        {({ index, style }) => (
          <div
            style={{ ...style, top: `${parseFloat(style.top) + 100}px` }}
            className="block overflow-hidden p-2 hover:overflow-visible"
            key={matchingIngredients[index].id}
          >
            <Link
              href={`/management/ingredients/${matchingIngredients[index].id}`}
              className={`whitespace-nowrap rounded-lg bg-white/30 p-1 text-gray-700 shadow hover:shadow-lg active:shadow-inner ${
                path?.includes(
                  `/management/ingredients/${matchingIngredients[index].id}/`
                ) ||
                path ===
                  `/management/ingredients/${matchingIngredients[index].id}`
                  ? "bg-primary-400 text-black"
                  : ""
              }`}
            >
              {matchingIngredients[index].name} -{" "}
              {matchingIngredients[index].used_last_month}
            </Link>
          </div>
        )}
      </List>
      <div
        id="search"
        className="absolute top-0 flex-none p-3 pt-2 backdrop-blur"
      >
        <form onSubmit={handleSubmit}>
          <label
            htmlFor="searchbar"
            className="mt-2 block pl-1 text-sm font-medium text-gray-700"
          >
            Hľadaj ingredienciu
          </label>
          <input
            type="text"
            name="searchbar"
            id="searchbar"
            className="focus:outline-primary my-2 block w-full rounded-full px-3 py-2  shadow-md hover:shadow-lg focus:shadow-lg sm:text-sm"
            placeholder={
              "napr: " +
              ingredients[Math.floor(Math.random() * ingredients.length)].name
            }
            value={search}
            onChange={handleSearch}
          />
        </form>
      </div>
    </div>
  );
}
