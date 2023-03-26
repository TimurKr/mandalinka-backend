import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

import Fuse from "fuse.js";

import { useRouter } from "next/navigation";

// import { Ingredient } from "@/components/fetching/ingredients_list";
import Button from "@/components/button";

import {
  DocumentNode,
  gql,
  useQuery,
  useSuspenseQuery_experimental as useSuspenseQuery,
} from "@apollo/client";
import Alert from "@/components/alert";
import Loading from "@/components/loading_element";
import Error from "@/components/error_element";
import TextInput from "@/components/form_elements/text";
import { Form, Formik } from "formik";

type Ingredient = {
  id: number;
  name: string;
  usageLastMonth: number;
  url: string;
  isActive: boolean;
  isInactive: boolean;
  isDeleted: boolean;
};

type IngredientsData = {
  ingredients: Ingredient[];
};

const ingredientsQuery = gql`
  query Ingredients {
    ingredients {
      id
      name
      usageLastMonth
      url
      isActive
      isInactive
      isDeleted
    }
  }
`;

export default function Search() {
  // Declare states

  const [search, setSearch] = useState("");
  const [matchingIngredients, setMatchingIngredients] = useState<Ingredient[]>(
    []
  );

  // Router for redirecting
  const router = useRouter();
  const path = usePathname();

  // Fetch data
  const { data, error } = useSuspenseQuery<IngredientsData>(ingredientsQuery, {
    errorPolicy: "ignore",
  });

  console.log("error: ", error, error?.message);

  // Fuse.js for searching
  const fuse = new Fuse(data.ingredients, { keys: ["name", "id"] });

  const currentIngredient = data.ingredients.find(
    (ingredient: Ingredient) =>
      path?.endsWith(`/management/ingredients/${ingredient.id}`) ||
      path?.includes(`/management/ingredients/${ingredient.id}/`)
  );

  function moveSelectedIngredientToTop(original: Ingredient[]): Ingredient[] {
    if (!currentIngredient) {
      return original;
    }

    const index = original.indexOf(currentIngredient);
    if (index !== -1) {
      original.splice(index, 1);
      original.unshift(currentIngredient);
    }

    return original;
  }

  function handleSearch(value: string): void {
    if (value === search && value !== "") {
      return;
    }
    setSearch(value);

    let results = data.ingredients;

    if (value !== "") {
      results = fuse.search(value).map((result) => result.item);
    }

    // Sort results to show the active first, then inactive, then deleted, then the rest
    // The current ingredient is always first
    results.sort((a, b) => {
      if (a.isActive && !b.isActive) {
        return -1;
      }
      if (!a.isActive && b.isActive) {
        return 1;
      }
      if (a.isInactive && !b.isInactive) {
        return -1;
      }
      if (!a.isInactive && b.isInactive) {
        return 1;
      }
      if (a.isDeleted && !b.isDeleted) {
        return -1;
      }
      if (!a.isDeleted && b.isDeleted) {
        return 1;
      }
      if (!a.isActive && !a.isDeleted && !a.isInactive) {
        return 1;
      }
      if (!b.isActive && !b.isDeleted && !b.isInactive) {
        return -1;
      }
      return 0;
    });
    results = moveSelectedIngredientToTop(results);
    setMatchingIngredients(results);
  }

  useEffect(() => {
    handleSearch(search);
    console.log("search: ", search);
  }, [search]);

  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>): void {
    event.preventDefault();
    if (matchingIngredients.length === 0) {
      return;
    }
    router.push(matchingIngredients[0].url);
  }

  return (
    <div className="flex h-full w-[15rem] flex-col">
      <div className="z-10 w-full flex-none p-3 backdrop-blur">
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
            className="focus:outline-primary my-2 block w-full rounded-full px-3 py-2 shadow-md hover:shadow-lg focus:shadow-lg sm:text-sm"
            placeholder={data?.ingredients[0].name}
            value={search}
            onChange={(event) => {
              handleSearch(event.target.value);
            }}
          />
        </form>
      </div>
      <div className="z-0 w-full flex-grow overflow-y-scroll">
        {matchingIngredients.length === 0 && (
          <Alert variant="warning">
            Nenašli sa žiadne výsledky pre hľadanie <strong>{search}</strong>
          </Alert>
        )}

        <ul className="h-full">
          {matchingIngredients.map((ingredient) => (
            <li key={ingredient.id} className="block p-2">
              <Button
                variant={
                  ingredient.isActive
                    ? "success"
                    : ingredient.isInactive
                    ? "warning"
                    : ingredient.isDeleted
                    ? "danger"
                    : "black"
                }
                dark={currentIngredient?.id === ingredient.id}
                href={ingredient.url}
                className={`inline ${
                  !ingredient.isActive &&
                  !ingredient.isInactive &&
                  !ingredient.isDeleted
                    ? "opacity-70"
                    : ""
                }`}
              >
                {ingredient.name}
              </Button>
            </li>
          ))}
        </ul>
      </div>
      <div className="z-10 w-full flex-none p-3 backdrop-blur">
        <Button variant="primary" dark href="/management/ingredients/new">
          Pridať novú ingredienciu
        </Button>
      </div>
    </div>
  );
}
