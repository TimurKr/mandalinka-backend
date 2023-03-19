import Search from "./search";

import fetchIngredients from "@/components/fetching/ingredients_list";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const ingredients = await fetchIngredients();

  return (
    <div className="flex h-full w-full">
      <div className="flex-none border-r border-gray-300">
        <Search ingredients={ingredients} />
      </div>
      <div className="h-full flex-auto overflow-auto p-2">{children}</div>
    </div>
  );
}
