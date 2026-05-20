import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { DashboardPage } from "../pages/DashboardPage";
import { LoginPage } from "../pages/LoginPage";
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
            <Route path="/referrals/new" element={<ReferralFormPage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
