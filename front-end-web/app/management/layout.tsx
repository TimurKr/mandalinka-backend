import Navigation from "./navigation";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <section className="bg-primary-100 flex h-screen w-screen">
      <div className="flex-none">
        <Navigation />
      </div>
      <div className="flex-auto">{children}</div>
    </section>
  );
}
