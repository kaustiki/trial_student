import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { useAuthStore } from "../store/authStore";
import { ReferralFormPage } from "./ReferralFormPage";

vi.mock("../services/referrals", () => ({
  getFormAccess: vi.fn().mockResolvedValue({
    role: "teacher",
    visible_sections: ["student", "referral", "teacher_details"],
    editable_sections: ["teacher_details"]
  }),
  createReferral: vi.fn()
}));

describe("ReferralFormPage", () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: {
        id: 1,
        name: "Demo Teacher",
        email: "teacher@example.com",
        role: "teacher",
        is_active: true
      }
    });
  });

  it("enables teacher-owned form fields for teachers", async () => {
    render(<ReferralFormPage />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /submit referral/i })).toBeEnabled();
    });
    expect(screen.getByLabelText(/admission number/i)).toBeEnabled();
    expect(screen.getByLabelText(/behavior issues/i)).toBeEnabled();
  });
});
