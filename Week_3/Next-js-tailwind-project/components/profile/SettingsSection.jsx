export default function SettingsSection({ title, children }) {
  return (
    <div className="space-y-6">
      <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
        {title}
      </h4>
      {children}
    </div>
  );
}
