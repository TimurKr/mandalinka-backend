import { ReactComponentElement } from "react";

import { XMarkIcon } from "@heroicons/react/24/outline";

export default function WarningAlert({
  children,
  onClose,
}: {
  children: React.ReactNode;
  onClose?: () => void;
}): ReactComponentElement<any> {
  return (
    <div
      className="flex justify-between rounded-xl border border-orange-600 p-2 text-orange-600"
      role="alert"
    >
      <span className="font-medium">{children}</span>
      {onClose && (
        <button
          className="text-orange-600 hover:text-orange-800"
          onClick={onClose}
          aria-label="Close"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      )}
    </div>
  );
}