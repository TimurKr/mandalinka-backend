"use client";

export default function Management() {
  return (
    <div className="grid h-full place-content-center">
      <p className="text-center text-lg">Manažment stránka.</p>
      <p className="flex justify-center text-neutral-600">
        <span className="material-symbols-rounded animate-move-left-right mr-3">
          arrow_back
        </span>
        Zvoľte si stránku v navigácii vľavo.
      </p>
    </div>
  );
}
