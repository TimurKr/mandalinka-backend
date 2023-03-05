"use client";

import { useEffect, useState } from "react";
import { FixedSizeList as List } from "react-window";
import { usePathname } from "next/navigation";

import Fuse from "fuse.js";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { Ingredient } from "@/components/fetching/ingredients_list";
import Button from "@/components/button";
import { IncomingMessage } from "http";

export default function Search({ ingredients }: { ingredients: Ingredient[] }) {
  // States for searching
  const [search, setSearch] = useState("");
  const [matchingIngredients, setMatchingIngredients] = useState<Ingredient[]>(
    []
  );

  // Fuse.js for searching
  const fuse = new Fuse(ingredients, { keys: ["name", "id"] });

  // Router for redirecting
  const router = useRouter();
  const path = usePathname();

  // Handle some things on the client side only
  const [placeholder, setPlaceholder] = useState("napr: ");
  const [windowHeight, setWindowHeight] = useState(0);
  useEffect(() => {
    setWindowHeight(window.innerHeight);
    setPlaceholder(
      "napr: " +
        ingredients[Math.floor(Math.random() * ingredients.length)].name
    );
    setMatchingIngredients(
      moveSelectedIngredientToTop(
        ingredients
          .slice()
          .sort((a, b) => b.usage_last_month - a.usage_last_month)
      )
    );
  }, []);

  function moveSelectedIngredientToTop(original: Ingredient[]): Ingredient[] {
    // Move the ingredient that is currently selected to the top of the list
    let id = -1;
    ingredients.forEach((ingredient) => {
      if (path?.includes(`/management/ingredients/${ingredient.id}`)) {
        id = ingredient.id;
      }
    });
    if (id === -1) {
      router.refresh();
    }

    const index = original.findIndex((ingredient) => ingredient.id === id);
    if (index !== -1) {
      const ingredient = original[index];
      original.splice(index, 1);
      original.unshift(ingredient);
    }

    return original;
  }

  function handleSearch(event: React.ChangeEvent<HTMLInputElement>): void {
    setSearch(event.target.value);

    let results = fuse.search(event.target.value).map((result) => result.item);
    if (results.length === 0) {
      results = ingredients
        .slice()
        .sort((a, b) => b.usage_last_month - a.usage_last_month);
    }

    setMatchingIngredients(moveSelectedIngredientToTop(results));
  }

  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>): void {
    event.preventDefault();
    if (matchingIngredients.length === 0) {
      return;
    }
    router.push(matchingIngredients[0].url);
  }

  return (
    <div className="relative h-full w-[15rem]">
      <div className="relative flex-grow">
        <div
          id="search"
          className="absolute top-0 z-10 w-full flex-none p-3 backdrop-blur"
        >
          <form onSubmit={handleSubmit}>
            <label
              htmlFor="searchbar"
              className="block pl-1 text-sm font-medium text-gray-700"
            >
              Hľadaj ingredienciu
            </label>
            <input
              type="text"
              name="searchbar"
              id="searchbar"
              autoComplete="off"
              className="focus:outline-primary my-2 block w-full rounded-full px-3 py-2  shadow-md hover:shadow-lg focus:shadow-lg sm:text-sm"
              placeholder={placeholder}
              value={search}
              onChange={handleSearch}
            />
          </form>
        </div>

        <List
          height={windowHeight - 70}
          itemCount={matchingIngredients.length}
          itemSize={37}
          width={"100%"}
          className="overflow-x-visible overscroll-auto"
        >
          {({ index, style }) => {
            let ingredient = matchingIngredients[index];

            let is_selected =
              path?.includes(`/management/ingredients/${ingredient.id}/`) ||
              path === `/management/ingredients/${ingredient.id}`;

            return (
              <div
                style={{
                  ...style,
                  top: `${parseFloat(style.top?.toString() || "0") + 100}px`,
                }}
                className="block overflow-hidden p-2 hover:overflow-visible"
                key={ingredient.id}
              >
                <Link
                  href={ingredient.url}
                  className={`focus:ring-primary focus:outline-primary focus:border-primary  whitespace-nowrap rounded-full p-1 px-2 shadow hover:shadow-lg active:shadow-inner 
                   ${
                     ingredient.is_active
                       ? is_selected
                         ? "bg-green-500"
                         : "text-green-700"
                       : ingredient.is_inactive
                       ? is_selected
                         ? "bg-yellow-400"
                         : "text-yellow-600"
                       : ingredient.is_deleted
                       ? is_selected
                         ? "bg-red-500"
                         : "text-red-500"
                       : is_selected
                       ? "bg-gray-400 text-black"
                       : "text-gray-500"
                   }`}
                >
                  {matchingIngredients[index].name} -{" "}
                  {matchingIngredients[index].usage_last_month}
                </Link>
              </div>
            );
          }}
        </List>
      </div>

      <div
        id="add_new"
        className="absolute bottom-0 z-10 w-full flex-none p-3 backdrop-blur"
      >
        <Button style="primary" dark href="/management/ingredients/new">
          Pridať novú ingredienciu
        </Button>
      </div>
    </div>
  );
}
