import {
  DocumentNode,
  gql,
  useSuspenseQuery_experimental as useSuspenseQuery,
} from "@apollo/client";
import { useField, Field, FieldHookConfig } from "formik";
import { useEffect } from "react";
import { isPropertySignature } from "typescript";
import ErrorMessage from "./error_message";

type SelectInputProps = FieldHookConfig<string | number> & {
  label: string;
  query_options_schema: DocumentNode;
  value_key?: string;
  label_key?: string;
};

const SelectInput: React.FC<SelectInputProps> = (props) => {
  const { data } = useSuspenseQuery(props.query_options_schema);

  const options = data[Object.keys(data)[0]].map((option: any) => ({
    value: option[props.value_key || "id"],
    label: option[props.label_key || "name"],
  }));

  const [field, meta, helper] = useField(props);

  // Raise error if value is not in options
  useEffect(() => {
    if (
      field.value &&
      !options.find((option: any) => option.value == field.value)
    ) {
      console.error(`Value ${field.value} not in options:`, options);
    }
  });

  return (
    <div className="relative">
      <select
        {...field}
        id={props.name}
        disabled={props.disabled}
        className="focus:border-primary focus:ring-primary block w-full rounded-lg border border-gray-300 bg-inherit p-2.5 pr-4 text-sm text-gray-900 focus:outline-none focus:ring-0 disabled:bg-black/10"
      >
        {!field.value && (
          <option value="" disabled>
            {props.label}
          </option>
        )}
        {options.map((option: any) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <label
        htmlFor={props.name}
        className="peer-focus:text-primary absolute top-2 left-1 z-10 origin-[0] -translate-y-4 scale-75 transform rounded-full px-2 text-sm text-gray-700 backdrop-blur-xl duration-300 peer-placeholder-shown:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-100 peer-focus:top-2 peer-focus:-translate-y-4 peer-focus:scale-75 peer-focus:px-2"
      >
        {props.label}
      </label>
      <ErrorMessage meta={meta} />
    </div>
  );
};

export default SelectInput;
