import { ReactComponentElement } from "react";

import { XMarkIcon } from "@heroicons/react/24/outline";

export default function SuccessAlert({
  children,
  onClose,
}: {
  children: React.ReactNode;
  onClose?: () => void;
}): ReactComponentElement<any> {
  return (
    <div
      className="flex justify-between rounded-xl border border-green-600 p-2 text-green-600"
      role="alert"
    >
      <span className="font-medium">{children}</span>
      {onClose && (
        <button
          className="text-green-600 hover:text-green-800"
          onClick={onClose}
          aria-label="Close"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      )}
    </div>
  );
}
