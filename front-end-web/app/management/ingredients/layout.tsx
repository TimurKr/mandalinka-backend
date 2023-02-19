import Search from "./search";

import getData from "./fetch_ingredients";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const ingredients = await getData();

  return (
    <div className="flex h-full w-full">
      <div className="flex-none border-r border-gray-300">
        <Search ingredients={ingredients} />
      </div>
      <div className="flex-auto p-2">{children}</div>
    </div>
  );
}
