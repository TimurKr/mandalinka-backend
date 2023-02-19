import { useField, Field } from "formik";

export const Select = ({
  label,
  name,
  options,
}: {
  label: string;
  name: string;
  options: { value: string; label: string }[];
}) => {
  const [field, meta, helper] = useField(name);
  const selectedOptions = field.value || [];
  return (
    <>
      <select
        id="countries"
        className="focus:border-primary focus:ring-primary block w-full rounded-lg border border-gray-300 bg-inherit p-2.5 pr-4 text-sm text-gray-900 focus:outline-none focus:ring-0"
      >
        <option selected>{label}</option>
        {options.map((option) => (
          <option value={option.value}>{option.label}</option>
        ))}
      </select>
    </>
  );
  return (
    <div>
      <div className="pb-2">{label}:</div>
      <div
        role="group"
        aria-labelledby="checkbox-group"
        className="flex flex-wrap justify-center gap-2"
      >
        {options.map((option) => (
          <span>
            <Field
              id={option.value}
              type="checkbox"
              name="alergens"
              value={option.value}
              className="peer hidden"
            />
            <label
              key={option.value}
              htmlFor={option.value}
              className="hover:bg-primary-200 peer-checked:bg-primary-400 cursor-pointer rounded-full p-1 px-2 hover:shadow peer-checked:shadow-sm"
            >
              {option.label}
            </label>
          </span>
        ))}
      </div>
    </div>
  );
};
