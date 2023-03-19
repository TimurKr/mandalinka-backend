import Search from "./search";

import fetchRecipeDesignsList from "@/components/fetching/recipe_designs_list";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const recipes = await fetchRecipeDesignsList();

  return (
    <div className="flex h-full w-full">
      <div className="flex-none border-r border-gray-300">
        <Search recipes={recipes} />
      </div>
      <div className="h-full flex-auto overflow-auto p-2">{children}</div>
    </div>
  );
}
