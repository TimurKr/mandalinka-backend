import { useRouter } from "next/navigation";

export default async function parseInvalidResponse(
  response: Response,
  setFieldError: (field: string, errorMsg: string) => void,
  setFormError: (errorMsg: string) => void,
  router?: ReturnType<typeof useRouter>,
  success_url?: string
): Promise<any> {
  let response_json = await response.json();

  if (!response.ok) {
    Object.keys(response_json).forEach((key: string) => {
      if (key === "non_field_errors") {
        setFormError(response_json[key]);
      } else {
        setFieldError(key, response_json[key]);
      }
    });
    console.log("Response: ", response_json);
  } else {
    console.log("Response ok: ", response_json);

    if (router && success_url) {
      setTimeout(() => {
        router.push(success_url);
      }, 250);
    }
  }

  return response_json;
}
