"use client";
import { useState } from "react";

export default function ToggleSwitch({ defaultOn = false, onChange }) {
  const [enabled, setEnabled] = useState(defaultOn);

  const toggle = () => {
    const newValue = !enabled;
    setEnabled(newValue);
    onChange && onChange(newValue);
  };

  return (
    <button
      onClick={toggle}
      className={`relative w-12 h-6 rounded-full transition-colors duration-300 ${
        enabled ? "bg-teal-400" : "bg-gray-300"
      }`}
    >
      <span
        className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow-md transition-transform duration-300 ${
          enabled ? "translate-x-6" : ""
        }`}
      />
    </button>
  );
}
