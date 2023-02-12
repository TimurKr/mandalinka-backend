import VersionSelector from "./version_selector";

export default function Layout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { id: string };
}) {
  return (
    <div className="h-full w-full p-2">
      <div>
        Detail ingrediencie {params.id}
        <VersionSelector ingrdient_id={params.id} />
      </div>
      <div>{children}</div>
    </div>
  );
}
