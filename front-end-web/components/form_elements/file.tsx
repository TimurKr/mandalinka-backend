"use client";

import Image from "next/image";

import { CloudArrowUpIcon } from "@heroicons/react/20/solid";

import { useField, FieldHookConfig } from "formik";
import ErrorMessage from "./error_message";

type FileInputProps = FieldHookConfig<File> & {
  label: string;
  thumbnail_width?: number;
  thumbnail_height?: number;
  initial_url?: string | null;
};

export const FileInput = ({ ...props }: FileInputProps) => {
  const [field, meta] = useField(props.name);

  console.log(field.value);

  return (
    <div className="flex w-full items-center justify-center">
      <label
        htmlFor={props.id || props.name}
        className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 "
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          {field.value || props.initial_url ? (
            <div className="mt-2">
              <div className="flex flex-col items-center">
                <Image
                  src={
                    field.value
                      ? URL.createObjectURL(field.value)
                      : props.initial_url
                      ? props.initial_url
                      : ""
                  }
                  alt="Selected image"
                  className="object-contain"
                  width={props.thumbnail_width || 200}
                  height={props.thumbnail_height || 200}
                />
                <span className="font-medium text-gray-900">
                  {field.value?.name}
                </span>
              </div>
            </div>
          ) : (
            <CloudArrowUpIcon className="h-10 w-10 text-gray-400" />
          )}
          <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
            <span className="font-semibold">Click to upload</span> or drag and
            drop
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            SVG, PNG, JPG or GIF (MAX. 800x400px)
          </p>
          <ErrorMessage meta={meta} />
        </div>
        <input
          type="file"
          id={props.id || props.name}
          onChange={(event) => {
            const file = event.currentTarget.files?.item(0);
            if (file) {
              field.onChange({
                target: { name: field.name, value: file },
              });
            }
            console.log(file);
          }}
          onBlur={field.onBlur}
          value={undefined}
          className="hidden"
        />
      </label>
    </div>
  );
};
