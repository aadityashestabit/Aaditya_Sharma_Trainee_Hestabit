"use client";

import ToggleSwitch from "../ToggleSwitch";
import SettingsSection from "./SettingsSection";

export default function PlatformSettings() {
  return (
    <div className="bg-white rounded-2xl max-w-sm max-h-110 h-full p-6  w-100 text-xs ">
      
      <h2 className="text-lg font-semibold text-gray-800">
        Platform Settings
      </h2>

      {/* ACCOUNT */}
      <SettingsSection title="Account">
        <div className="flex items-center justify-between">
          <ToggleSwitch defaultOn />
          <span className="text-gray-500">
            Email me when someone follows me
          </span>
        </div>

        <div className="flex items-center justify-between ">
          <ToggleSwitch />
          <span className="text-gray-500">
            Email me when someone answers on my post
          </span>
        </div>

        <div className="flex items-center justify-between mb-5">
          <ToggleSwitch defaultOn />
          <span className="text-gray-500 mb-4">
            Email me when someone mentions me
          </span>
        </div>
      </SettingsSection>

      {/* APPLICATION */}
      <SettingsSection title="Application">
        <div className="flex items-center justify-between ">
          <ToggleSwitch />
          <span className="text-gray-500">
            New launches and projects
          </span>
        </div>

        <div className="flex items-center justify-between">
          <ToggleSwitch />
          <span className="text-gray-500">
            Monthly product updates
          </span>
        </div>

        <div className="flex items-center justify-between">
          <ToggleSwitch defaultOn />
          <span className="text-gray-500">
            Subscribe to newsletter
          </span>
        </div>
      </SettingsSection>

    </div>
  );
}
