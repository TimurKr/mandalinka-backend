export function BorderedElement({
  children,
  className,
  title,
}: {
  children: React.ReactNode;
  className?: string;
  title?: string;
}) {
  return (
    <div
      className={
        className +
        " relative h-full w-full rounded-xl border border-gray-500 p-2"
      }
    >
      {title && (
        <div className="absolute top-0 left-1 -translate-y-1/2 rounded-xl px-2 backdrop-blur-3xl">
          <h4 className="text-xs">{title}</h4>
        </div>
      )}
      {children}
    </div>
  );
}
