import { useField, Field } from "formik";
import ErrorMessage from "./error_message";

export const MultiSelect = ({
  label,
  name,
  options,
}: {
  label: string;
  name: string;
  options: { value: string | number; label: string }[];
}) => {
  const [field, meta, helper] = useField(name);

  return (
    <div>
      <div className="pb-2">{label}:</div>
      <div
        role="group"
        aria-labelledby="checkbox-group"
        className="flex flex-wrap justify-center gap-2"
      >
        {options.map((option) => (
          <span key={option.value}>
            <input
              id={option.value?.toString()}
              type="checkbox"
              name={name}
              value={option.value}
              checked={field.value.includes(option.value)}
              onChange={(e: any) => {
                const checked = e.target.checked;
                const value = option.value;
                const currentValue = field.value;
                let newValue;
                if (checked) {
                  newValue = [...currentValue, value];
                } else {
                  newValue = currentValue.filter((v: string) => v !== value);
                }
                helper.setValue(newValue);
              }}
              className="peer hidden"
            />
            <label
              key={option.value}
              htmlFor={option.value?.toString()}
              className="hover:bg-primary-200 peer-checked:bg-primary-400 peer-checked:hover:bg-primary-300 cursor-pointer rounded-full p-1 px-2 hover:shadow peer-checked:shadow-md"
            >
              {option.label}
            </label>
          </span>
        ))}
      </div>
      <ErrorMessage meta={meta} />
    </div>
  );
};
