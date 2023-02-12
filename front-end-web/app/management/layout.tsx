import Navigation from "./navigation";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <section className="flex h-screen w-screen overflow-hidden bg-slate-100">
      <div className="z-10 flex-none shadow-xl">
        <Navigation />
      </div>
      <div className="flex-auto">{children}</div>
    </section>
  );
}
