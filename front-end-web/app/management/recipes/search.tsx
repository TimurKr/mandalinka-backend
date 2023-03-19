"use client";

import { useEffect, useState } from "react";
import { FixedSizeList as List } from "react-window";
import { usePathname } from "next/navigation";

import Fuse from "fuse.js";

import Link from "next/link";
import { useRouter } from "next/navigation";

import Button from "@/components/button";
import { RecipeDesign } from "@/components/fetching/recipe_designs_list";

export default function Search({ recipes }: { recipes: RecipeDesign[] }) {
  // States for searching
  const [search, setSearch] = useState("");
  const [matchingRecipes, setMatchingRecipes] = useState<RecipeDesign[]>([]);

  // Fuse.js for searching
  const fuse = new Fuse(recipes, { keys: ["name", "id"] });

  // Router for redirecting
  const router = useRouter();
  const path = usePathname();

  // Handle some things on the client side only
  const [placeholder, setPlaceholder] = useState("napr: ");
  const [windowHeight, setWindowHeight] = useState(0);

  useEffect(() => {
    setWindowHeight(window.innerHeight);
    setPlaceholder(
      "napr: " + recipes[Math.floor(Math.random() * recipes.length)]?.name
    );
    setMatchingRecipes(
      moveSelectedRecipeToTop(recipes.slice().sort((a, b) => b.id - a.id))
    );
  }, []);

  function moveSelectedRecipeToTop(original: RecipeDesign[]): RecipeDesign[] {
    // Move the ingredient that is currently selected to the top of the list
    let id = -1;
    recipes.forEach((recipe) => {
      if (path?.includes(`/management/recipe-designs/${recipe.id}`)) {
        id = recipe.id;
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
      results = recipes.slice().sort((a, b) => b.id - a.id);
    }

    setMatchingRecipes(moveSelectedRecipeToTop(results));
  }

  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>): void {
    event.preventDefault();
    if (matchingRecipes.length === 0) {
      return;
    }
    router.push(matchingRecipes[0].url);
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
              Hľadaj recept
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

        {recipes.length == 0 ? (
          <div className="pt-28 text-center">Žiadne recepty</div>
        ) : (
          <List
            height={windowHeight - 70}
            itemCount={matchingRecipes.length}
            itemSize={37}
            width={"100%"}
            className="overflow-x-visible overscroll-auto"
          >
            {({ index, style }) => {
              let recipe = matchingRecipes[index];

              let is_selected =
                path?.includes(`/management/ingredients/${recipe.id}/`) ||
                path === `/management/ingredients/${recipe.id}`;

              return (
                <div
                  style={{
                    ...style,
                    top: `${parseFloat(style.top?.toString() || "0") + 100}px`,
                  }}
                  className="block overflow-hidden p-2 hover:overflow-visible"
                  key={recipe.id}
                >
                  <Button
                    href={recipe.url}
                    variant={
                      recipe.is_active
                        ? "success"
                        : recipe.is_inactive
                        ? "warning"
                        : recipe.is_deleted
                        ? "danger"
                        : "black"
                    }
                    dark={is_selected}
                    className={`inline ${
                      !recipe.is_active &&
                      !recipe.is_inactive &&
                      !recipe.is_deleted
                        ? "opacity-70"
                        : ""
                    }`}
                  >
                    {matchingRecipes[index].name}
                  </Button>
                  {/* </Link> */}
                </div>
              );
            }}
          </List>
        )}
      </div>

      <div
        id="add_new"
        className="absolute bottom-0 z-10 w-full flex-none p-3 backdrop-blur"
      >
        <Button variant="primary" dark href="/management/recipes/new">
          Vyrobiť nový recept
        </Button>
      </div>
    </div>
  );
}
