import { Transition } from "@headlessui/react";
import { Fragment } from "react";

export default function Modal({
  isShowing,
  setIsShowing,
  children,
}: {
  isShowing: boolean;
  setIsShowing?: (isShowing: boolean) => void;
  children: React.ReactNode;
}) {
  return (
    <Transition
      show={isShowing}
      enter="transition-opacity duration-500"
      enterFrom="opacity-0"
      enterTo="opacity-100"
      leave="transition-opacity duration-500"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
    >
      <div
        className="fixed top-0 left-0 z-50 grid h-full w-full place-content-center bg-black/10 backdrop-blur-sm"
        onClick={() => setIsShowing && setIsShowing(false)}
      >
        {children}
      </div>
    </Transition>
  );
}
