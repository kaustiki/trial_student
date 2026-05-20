import { describe, expect, it } from "vitest";

import { titleize } from "./labels";

describe("titleize", () => {
  it("turns snake case into display text", () => {
    expect(titleize("student_counsellor")).toBe("Student Counsellor");
  });
});
