import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";

type BaseProps = {
  label: string;
  error?: string;
};

type InputProps = BaseProps &
  InputHTMLAttributes<HTMLInputElement> & {
    multiline?: false;
  };

type TextareaProps = BaseProps &
  TextareaHTMLAttributes<HTMLTextAreaElement> & {
    multiline: true;
  };

type FieldProps = InputProps | TextareaProps;

export function Field({ label, error, multiline, ...props }: FieldProps) {
  const controlClass =
    "mt-1 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-ocean focus:ring-2 focus:ring-cyan-100";

  return (
    <label className="block text-sm font-medium text-slate-700">
      {label}
      {multiline ? (
        <textarea
          className={`${controlClass} min-h-24 resize-y`}
          {...(props as TextareaHTMLAttributes<HTMLTextAreaElement>)}
        />
      ) : (
        <input className={controlClass} {...(props as InputHTMLAttributes<HTMLInputElement>)} />
      )}
      {error ? <span className="mt-1 block text-xs text-red-600">{error}</span> : null}
    </label>
  );
}
