"use client";

import { Suspense } from "react";
import Loading from "@/components/loading_element";
import Search from "./search";
import {
  ApolloClient,
  ApolloProvider,
  HttpLink,
  InMemoryCache,
  SuspenseCache,
} from "@apollo/client";
import { getClient } from "@/components/apollo_client";

const suspenseCache = new SuspenseCache();

const client = new ApolloClient({
  link: new HttpLink({
    uri: `http://localhost:8000/graphql`,
  }),
  cache: new InMemoryCache(),
});

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-full w-full">
      <ApolloProvider client={client} suspenseCache={suspenseCache}>
        <div className="flex-none border-r border-gray-300">
          <Suspense fallback={<Loading />}>
            <Search />
          </Suspense>
        </div>
        <div className="h-full flex-auto overflow-auto p-2">{children}</div>
      </ApolloProvider>
    </div>
  );
}
