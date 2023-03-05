import Search from "./search";

import fetchIngredientsList from "@/components/fetching/ingredients_list";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const ingredients = await fetchIngredientsList();

  return (
    <div className="flex h-full w-full">
      <div className="flex-none border-r border-gray-300">
        <Search ingredients={ingredients} />
      </div>
      <div className="grid flex-auto place-content-center p-2">{children}</div>
    </div>
  );
}
