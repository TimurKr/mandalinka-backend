import { createMachine, assign } from "xstate";

const fetchDataMachine =
  /** @xstate-layout N4IgpgJg5mDOIC5QDMwBcDGALAIgQzTwDpVMsBLAOygGIIB7SsIqgN3oGtnTt9CBtAAwBdRKAAO9WOTTlGYkAA9EAFkEAmIivUBWddoBsATkEBGfUYA0IAJ6rBRAOz6DADkc6j6g44OmdOgC+gdY8uATEYVS0YABOsfSxROIANgTIiQC2JOi8EUKiSCCS0rLyRcoIagDMRIJGAWoqjq7GOtXWdgimBipa6qauQ2aOGoJuwaG54YREsACuGBhwsDQAYgCiACoAwgASBQolMnKUCpXeBkQG49UGnoI6NzqmnYgAtANEOoIqTR69PTVPSTEBhPiRPDkFI0Q5FY5lM4VRABHREIxeVwDIY6FRuKy2RDVQSudHEl69IymapGVyg8EREhQmGKWCENDMPDIDmxAAUpkEgoAlDQGbNkMy4RIpCdyqBKtV1I4iPpBuYlYZXCodG8EPpaq5PNUWqMTK4jPTphCmdD5rEwOttvspcUZYjzohvA4fD6BsTfK9CQhiVc3I8Bo1mljgiEQJR6BA4AoxXgjm7Th7uiYiNV3H4VK4NKZqeoOkH3gLSRjTCZVS91K1LWRrVFqGnShnkXrczm86YC0WS2WukY+v51EZqv3zWrHI4m3lZgslit27KkfLEH4HBiMVPBCGzAZdQZNNTHP5TB4p09cSoFzNIdC1+6u6eruZBn7qnir45dYMaKuD+NLOMB2ragYD4tsydpgC+nablUwJEP2NKtDSpZ+MORLjNcF79vq-YFjGgRAA */
  createMachine({
    id: "fetchData",
    initial: "fetching",
    context: {
      url: undefined,
      data: null,
      tries: 0,
      maxTries: 2,
    },
    states: {
      fetching: {
        invoke: {
          id: "fetchData",
          src: (context) =>
            fetch(context.url).then((response) => response.json()),
          onDone: {
            target: "success",
            actions: assign({
              data: (context, event) => event.data,
              tries: 0,
            }),
          },
          onError: {
            target: "fail",
            actions: assign({
              tries: (context) => context.tries + 1,
            }),
          },
        },
      },

      success: {
        on: {
          FETCH: "fetching",
        },
      },

      fail: {
        always: {
          target: "failure",
          cond: (context) => context.tries >= context.maxTries,
        },
        after: {
          1000: "fetching",
        },
      },

      failure: {
        on: {
          FETCH: "fetching",
        },
      },
    },
  });

export default fetchDataMachine;
