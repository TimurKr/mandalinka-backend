import { ReactComponentElement } from "react";

import { XMarkIcon } from "@heroicons/react/24/outline";

export default function DangerAlert({
  children,
  onClose,
}: {
  children: React.ReactNode;
  onClose?: () => void;
}): ReactComponentElement<any> {
  return (
    <div
      className="flex justify-between rounded-xl border border-red-600 p-2 text-red-600"
      role="alert"
    >
      <span className="font-medium">{children}</span>
      {onClose && (
        <button
          className="text-red-600 hover:text-red-800"
          onClick={onClose}
          aria-label="Close"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      )}
    </div>
  );
}
