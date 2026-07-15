import { NavLink, Outlet } from "react-router-dom";
import { LayoutDashboard, FileUp, Briefcase, History, LogOut, ScanSearch } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/upload-resume", label: "Upload Resume", icon: FileUp },
  { to: "/upload-jd", label: "Upload Job", icon: Briefcase },
  { to: "/history", label: "History", icon: History },
];

export default function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="flex min-h-screen bg-paper">
      <aside className="flex w-60 shrink-0 flex-col bg-ink text-paper">
        <div className="flex items-center gap-2 px-5 py-6">
          <ScanSearch className="size-6 text-signal" strokeWidth={2.2} />
          <span className="font-display text-lg font-extrabold tracking-tight">
            Resume<span className="text-signal">Scan</span>
          </span>
        </div>

        <nav className="flex flex-1 flex-col gap-1 px-3">
          {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium font-body transition-colors",
                  isActive
                    ? "bg-white/10 text-white"
                    : "text-paper/70 hover:bg-white/5 hover:text-white"
                )
              }
            >
              <Icon className="size-4" strokeWidth={2} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-white/10 px-5 py-4">
          <p className="truncate text-xs text-paper/60">{user?.email}</p>
          <p className="font-data text-[10px] uppercase tracking-wider text-signal">
            {user?.role}
          </p>
          <button
            onClick={logout}
            className="mt-3 flex items-center gap-2 text-xs font-medium text-paper/70 hover:text-white"
          >
            <LogOut className="size-3.5" />
            Sign out
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-6xl px-8 py-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
