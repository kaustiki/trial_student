import { titleize } from "../utils/labels";

type StatusPillProps = {
  status: string;
};

export function StatusPill({ status }: StatusPillProps) {
  return (
    <span className="inline-flex items-center rounded-md bg-cyan-50 px-2.5 py-1 text-xs font-semibold text-ocean ring-1 ring-cyan-200">
      {titleize(status)}
    </span>
  );
}
