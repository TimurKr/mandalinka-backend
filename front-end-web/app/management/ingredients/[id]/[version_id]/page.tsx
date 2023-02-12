export default function IngredientVersion({
  params,
}: {
  params: { id: string; version_id: string };
}) {
  return (
    <div>
      Detail ingrediencie {params.id}, verzie {params.version_id}
    </div>
  );
}
