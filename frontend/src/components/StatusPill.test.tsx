import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { StatusPill } from "./StatusPill";

describe("StatusPill", () => {
  it("renders a readable referral status label", () => {
    render(<StatusPill status="pending_review" />);

    expect(screen.getByText("Pending Review")).toBeInTheDocument();
  });
});
