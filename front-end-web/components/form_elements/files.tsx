"use client";

import Image from "next/image";

import { useField, FieldHookConfig } from "formik";

type FileInputProps = FieldHookConfig<FileList> & {
  label: string;
};

export const FileInput = ({ label, ...props }: FileInputProps) => {
  const [field, meta] = useField<FileList>(props);

  return (
    <div className="flex w-full items-center justify-center">
      <label
        htmlFor={props.id || props.name}
        className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 "
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          {field.value && field.value.length > 0 ? (
            <div className="mt-2">
              {Array.from(field.value).map((file: File) => (
                <div key={file.name} className="flex flex-col items-center">
                  <Image
                    src={URL.createObjectURL(file)}
                    alt="Selected image"
                    className="object-contain"
                    width={100}
                    height={100}
                  />
                  <span className="font-medium text-gray-900">{file.name}</span>
                </div>
              ))}
            </div>
          ) : (
            <svg
              aria-hidden="true"
              className="mb-3 h-10 w-10 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              ></path>
            </svg>
          )}
          <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
            <span className="font-semibold">Click to upload</span> or drag and
            drop
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            SVG, PNG, JPG or GIF (MAX. 800x400px)
          </p>
          {meta.touched && meta.error ? (
            <p className="mt-2 text-sm text-red-600">{meta.error}</p>
          ) : null}
        </div>
        <input
          type="file"
          id={props.id || props.name}
          onChange={(event) => {
            const files = event.currentTarget.files;
            if (files) {
              field.onChange({
                target: { name: field.name, value: files },
              });
            }
          }}
          onBlur={field.onBlur}
          value={undefined}
          className="hidden"
        />
      </label>
    </div>
  );
  return (
    <label className="block text-sm font-medium text-gray-700">
      {label}
      <div className="mt-1 flex justify-center rounded-md border-2 border-dashed border-gray-300 px-6 pt-5 pb-6">
        <div className="space-y-1 text-center">
          <div className="flex text-sm text-gray-600">
            <label
              htmlFor="file-upload"
              className="relative cursor-pointer rounded-md bg-white font-medium text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:text-indigo-500"
            >
              <span>Upload a file</span>
              <input
                type="file"
                id={props.id || props.name}
                onChange={(event) => {
                  const files = event.currentTarget.files;
                  if (files) {
                    field.onChange({
                      target: { name: field.name, value: files },
                    });
                  }
                }}
                onBlur={field.onBlur}
                value={undefined}
                hidden
              />
            </label>
            <p className="pl-1">or drag and drop</p>
          </div>
          <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
        </div>
      </div>
      {meta.touched && meta.error ? (
        <div className="mt-2 text-sm text-red-600">{meta.error}</div>
      ) : null}
      {field.value && field.value.length > 0 && (
        <div className="mt-2">
          {Array.from(field.value).map((file: File) => (
            <div key={file.name} className="flex items-center">
              <span className="font-medium text-gray-900">{file.name}</span>
              <img
                src={URL.createObjectURL(file)}
                alt=""
                className="ml-2 h-8 w-8 object-contain"
              />
            </div>
          ))}
        </div>
      )}
    </label>
  );
};
