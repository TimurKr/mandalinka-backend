"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

import Button from "@/components/button";
import DangerAlert from "@/components/alerts/danger";

export default function ActionPanel({
  delete_url,
  edit_url,
}: {
  delete_url: string;
  edit_url?: string;
}) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [isFetching, setIsFetching] = useState(false);
  const [message, setMessage] = useState("");

  const isMutating = isFetching || isPending;

  // async function onDelete(event: React.MouseEvent<HTMLButtonElement>) {
  //   console.log("Deleting ingredient");

  //   setIsFetching(true);
  //   const res = await fetch(delete_url, {
  //     method: "DELETE",
  //   });
  //   setIsFetching(false);

  //   if (res.ok) {
  //     startTransition(() => {
  //       // TODO: Refresh the search bar on the left of the page
  //       router.push("/management/ingredients/deleted");
  //     });
  //   } else {
  //     let res_json = await res.json();

  //     setMessage(res_json.detail);
  //   }
  // }

  return (
    <>
      <div className="flex flex-wrap justify-end gap-2">
        {edit_url && (
          <div className="flex-none">
            <Button style="black" href={edit_url} disabled={isMutating}>
              Edit
            </Button>
          </div>
        )}
        {/* <div className="flex-none">
          <Button style="danger" dark onClick={onDelete} disabled={isMutating}>
            Deaktivovať
          </Button>
        </div> */}
      </div>
      {message && (
        <>
          <DangerAlert onClose={() => setMessage("")}>{message}</DangerAlert>
        </>
      )}
    </>
  );
}
