import { useField, Field } from "formik";
import { useEffect } from "react";
import ErrorMessage from "./error_message";

export const Select = ({
  label,
  name,
  options,
}: {
  label: string;
  name: string;
  options: { value: string | number; label: string }[];
}) => {
  const [field, meta, helper] = useField(name);

  // Raise error if value is not in options
  useEffect(() => {
    if (field.value && !options.find((option) => option.value == field.value)) {
      console.error(`Value ${field.value} not in options:`, options);
    }
  });

  return (
    <>
      <select
        id={name}
        {...field}
        className="focus:border-primary focus:ring-primary block w-full rounded-lg border border-gray-300 bg-inherit p-2.5 pr-4 text-sm text-gray-900 focus:outline-none focus:ring-0"
      >
        {!field.value && (
          <option value="" disabled>
            Zvolte jednotku
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <ErrorMessage meta={meta} />
    </>
  );
};
