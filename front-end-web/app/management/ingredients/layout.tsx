import Search from "./search";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-full w-full">
      <div className="flex-none border-r border-gray-300">
        <Search />
      </div>
      <div className="flex-auto">{children}</div>
    </div>
  );
}
