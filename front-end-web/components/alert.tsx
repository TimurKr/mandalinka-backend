import { ReactComponentElement } from "react";

import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  NoSymbolIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";

export default function Alert({
  children,
  version,
  onClose,
  className,
  icon = true,
}: {
  children: React.ReactNode;
  version: "danger" | "warning" | "success" | "black" | "primary" | "secondary";
  onClose?: () => void;
  className?: string;
  icon?: boolean | JSX.Element;
}): ReactComponentElement<any> {
  return (
    <div
      className={`${className} m-2 flex items-center gap-2 rounded-xl border p-2 ${
        version === "danger"
          ? "border-red-600 text-red-600"
          : version === "warning"
          ? "border-yellow-600 text-yellow-600"
          : version === "success"
          ? "border-green-600 text-green-600"
          : version === "black"
          ? "border-gray-600 text-gray-600"
          : version === "primary"
          ? "border-primary-600 text-primary"
          : version === "secondary"
          ? "border-secondary-600 text-secondary"
          : ""
      }`}
      role="alert"
    >
      {icon == true ? (
        version === "danger" ? (
          <ExclamationCircleIcon className="h-6 w-6" aria-hidden="true" />
        ) : version === "warning" ? (
          <ExclamationTriangleIcon className="h-6 w-6" aria-hidden="true" />
        ) : version === "success" ? (
          <CheckCircleIcon className="h-6 w-6" aria-hidden="true" />
        ) : (
          <NoSymbolIcon className="h-6 w-6" aria-hidden="true" />
        )
      ) : icon ? (
        icon
      ) : (
        ""
      )}
      <span className="grow font-medium">{children}</span>
      {onClose && (
        <button
          className="rounded-md p-0.5 hover:bg-black/5"
          onClick={onClose}
          aria-label="Close"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      )}
    </div>
  );
}
