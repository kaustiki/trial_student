import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { DashboardPage } from "../pages/DashboardPage";
import { LoginPage } from "../pages/LoginPage";
import { ReferralDetailPage } from "../pages/ReferralDetailPage";
import { ReferralFormPage } from "../pages/ReferralFormPage";
import { ProtectedRoute } from "./ProtectedRoute";

export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route index element={<DashboardPage />} />
            <Route
              element={<ProtectedRoute allowedRoles={["teacher", "admin"]} />}
            >
              <Route path="/referrals/new" element={<ReferralFormPage />} />
            </Route>
            <Route path="/referrals/:id" element={<ReferralDetailPage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
