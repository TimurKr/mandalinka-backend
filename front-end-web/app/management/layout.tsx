import Navigation from "./navigation";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <section id="layout">
      <Navigation />
      {children}
    </section>
  );
}
